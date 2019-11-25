function loadPost(data) {
    const header = document.getElementById('city')
    const city = document.createElement('h2')
    header.append(city)
    city.innerHTML = data[0][8].toUpperCase()

    var num = 0
    const div = document.getElementById('listings')
    const buildList = (listing) => {
        console.log(num)
        const newrow = document.createElement('div')
        const oldrow = $('.row').prev()
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
        a.setAttribute('href', listing[3])
        a.setAttribute('class', 'btn btn-primary')
        icon.setAttribute('class', 'icon-input-btn glyphicon glyphicon-heart-empty')
        
        h3.innerHTML = listing[7]
        price.innerHTML = listing[5]
        if (listing[2]) beds.innerHTML = listing[2] + " Beds"
        if (listing[1]) baths.innerHTML = listing[1] + " Baths"

        a.innerHTML = "View on Craigslist"
    }
    data.forEach(listing => buildList(listing))
}

$(document).ready(function () 
{
    $.ajax({
        url:"http://localhost:5000/postdata",
        dataType: 'json',
        headers: {  
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        }, 
        success:function(json){
            loadPost(json);
        },
        error:function(request, error){
            console.log(error); //Should be removed after dev phase
        }
    });
});
