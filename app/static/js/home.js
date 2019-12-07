// check if an element is in a 2d list
function exists(arr, search) {
    return arr.some(row => row.includes(search));
}

function loadPost(data) {
    document.getElementById("listings").innerHTML = "";
    var favorite = 0
    listings = data['listings']
    fav = data['favorites']
    
    document.getElementById('prev').setAttribute('onclick', 'load_home(\'prev_' + listings[listings.length-1]['postingid'] + '\')')
    document.getElementById('next').setAttribute('onclick', 'load_home(\'next_' + listings[listings.length-1]['postingid'] + '\')')

    document.getElementById("gobutton").setAttribute('onclick', 'load_home(\'first\')')

    var num = 0
    const div = document.getElementById('listings')
    const buildList = (listing) => {
        const newrow = document.createElement('div')
        oldrow = $('.row')
        const col = document.createElement('div')
        const card = document.createElement('div')
        const header = document.createElement('div')
        const body = document.createElement('div')
        const h3 = document.createElement('h3')
        const price = document.createElement('h3')
        const bedbath = document.createElement('div')
        const beds = document.createElement('p')
        const baths = document.createElement('p')
        const link = document.createElement('div')
        const a = document.createElement('a')
        const icon = document.createElement('span')

        if(num % 4 == 0) {
            div.append(newrow)
            newrow.append(col)
            newrow.setAttribute('class', 'row')
            oldrow = newrow
        } else {
            oldrow.append(col)
        }
        num += 1
        col.append(card)
        card.append(header)
        card.append(body)
        header.append(h3)
        body.append(price)
        body.append(bedbath)
        bedbath.append(beds)
        bedbath.append(baths)
        card.append(link)
        link.append(a)
        link.append(icon)

        col.setAttribute('class', 'col-sm-3') 
        card.setAttribute('class', 'card')
        header.setAttribute('class', 'card-header')
        body.setAttribute('class', 'card-body')
        h3.setAttribute('class', 'card-title')

        price.setAttribute('class', 'card-text column')
        price.setAttribute('id', 'price')

        bedbath.setAttribute('class', 'card-text column')
        bedbath.setAttribute('id', 'bedbath')

        link.setAttribute('class', 'card-body')
        link.setAttribute('id', 'craig-link')
        a.setAttribute('href', listing['url'])
        a.setAttribute('class', 'btn btn-primary')

        icon.setAttribute('id', 'heart'+num)
        if (exists(fav, ("potato", listing['postingid']))) {
            favorite = 1
            icon.setAttribute('class', 'icon-input-btn glyphicon glyphicon-heart heart-selected')
        }
        else {
            icon.setAttribute('class', 'icon-input-btn glyphicon glyphicon-heart-empty')
        }
        
        h3.innerHTML = listing['title']
        price.innerHTML = listing['price']
        if (listing['beds']) beds.innerHTML = listing['beds'] + " Beds"
        if (listing['baths']) baths.innerHTML = listing['baths'] + " Baths"

        a.innerHTML = "View on Craigslist"
        document.getElementById('heart'+num).setAttribute('onclick', 'add_to_favorites(\'' + listing['postingid'] + '\', \'' + num +'\')')
    }
    listings.forEach(listing => buildList(listing))
}

function add_to_favorites(postingid, num, favorite) {
    $.ajax({
        url:"http://localhost:5000/add_favorite?postingid="+postingid,
        dataType: 'json',
        headers: {  
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        },
        success:function(resp) {
            if (resp['error'] == undefined){
                if (document.getElementById('heart'+num).classList.contains('heart-selected')) {
                    document.getElementById('heart'+num).classList.add('glyphicon-heart-empty')
                    document.getElementById('heart'+num).classList.remove('heart-selected', 'glyphicon-heart')

                } else  {
                    document.getElementById('heart'+num).classList.add('class', 'heart-selected', 'glyphicon-heart')
                    document.getElementById('heart'+num).classList.remove('class', 'glyphicon-heart-empty')
                }
            }
            else {
                console.log(resp['error'])
            }
        },
        error: function(request, error) {
            console.log(error)
        }
    })
}

function load_home(postingid) 
{
    city = document.getElementById("city_entry").value
    beds = document.getElementById("beds_entry").value
    url = (beds) ? "http://localhost:5000/homedata?city="+city+"&beds="+beds+"&postingid="+postingid : 
        "http://localhost:5000/homedata?city="+city+"&postingid="+postingid
    $.ajax({
        url: url,
        dataType: 'json',
        headers: {  
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        }, 
        success:function(json){
            loadPost(json)
        },
        error:function(request, error){
            console.log(error)
        }
    });
}

$(document).ready(
    load_home('first')
);
