// check if an element is in a 2d list
function exists(arr, search) {
    return arr.some(row => row.includes(search));
}

function loadPost(json) {
    var tot = 0
    for (key in json) {
        var num = 0
        data = json[key]
        var favorite = (key === 'favorites') ? 1 : 0
        const div = document.getElementById(key)

        // adding the similar items header only if there are similar posts
        if(!favorite) {
            if(json['similar'].length >= 1) {
                const similar_header = document.createElement('div')
                similar_header.setAttribute('class', 'header')
                similar_header.innerHTML = "You may also like.."
                div.append(similar_header)
            }
        }
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
            a.setAttribute('href', listing[12])
            a.setAttribute('class', 'btn btn-primary')

            tot+=1
            icon.setAttribute('id', 'heart'+tot)
            if(favorite) {
                icon.setAttribute('class', 'icon-input-btn glyphicon glyphicon-heart heart-selected')
            }else {
                icon.setAttribute('class', 'icon-input-btn glyphicon glyphicon-heart-empty')
            }
            h3.innerHTML = listing[11]
            price.innerHTML = listing[9]
            if (listing[2]) beds.innerHTML = listing[2] + " Bed"
            if (listing[1]) baths.innerHTML = listing[1] + " Bath"

            a.innerHTML = "View on Craigslist"
            document.getElementById('heart'+tot).setAttribute('onclick', 'add_to_favorites(\'' + listing[0] + '\', \'' + tot +'\')')
        }
        data.forEach(listing => buildList(listing))
    }
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

$(document).ready(function () 
{
    $.ajax({
        url:"http://localhost:5000/favoritesdata",
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
});
