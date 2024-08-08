const search = document.getElementById('search')

function slideLeft(){

    drop = document.getElementById('dropdown') ;
    document.getElementById('menuIcon2').style.display = 'block' ; 
    document.getElementById('menuIcon').style.display = 'none' ; 
    r = -400 ;
    
    function slide(){ 
      r += 10 ;
      drop.style.right = String(r) + 'px';
      console.log(drop.style.right)
      if(r < 20){ 
         window.requestAnimationFrame(slide);
      }
    }
    
    slide();
    
    }
    
function slideRight(){

drop = document.getElementById('dropdown') ;
document.getElementById('menuIcon2').style.display = 'none' ; 
document.getElementById('menuIcon').style.display = 'block' ; 
r = 10 ;

function slide(){ 
    r -= 10 ;
    drop.style.right = String(r) + 'px';
    console.log(drop.style.right)
    if(r > -400){ 
        window.requestAnimationFrame(slide);
    }
}

slide();

}

function goBack(){
    allBooks = Array.from(document.getElementsByClassName('book'));
    document.getElementById('searchMsg').style.display = 'none';
    document.getElementById('welcome').style.display = 'block';
    for (var i = 0; i < allBooks.length; i++) {
    allBooks[i].style.display = 'flex';
    }
    search.value = '';
}

search.addEventListener('keydown', function(event){ 
    if (event.key === 'Enter') {
        let book = search.value.toLowerCase();
        allBooks = Array.from(document.getElementsByClassName('book'));
        document.getElementById('searchMsg').style.display = 'block';
        document.getElementById('welcome').style.display = 'none';
        for (var i = 0; i < allBooks.length; i++) {
        if(!(allBooks[i].id.toLowerCase().includes(book))){
            allBooks[i].style.display = 'none';
        } else {
            allBooks[i].style.display = 'flex';
        }
        }
        } 
    }
)

function goToAvailableBooks() { 
    el = document.getElementById("_availableBooks");
    var rect = el.getBoundingClientRect();
    window.scrollTo(0, rect.top + window.scrollY - 140);
}

function goToUploadedBooks() { 
    el = document.getElementById("_uploadedBooks");
    var rect = el.getBoundingClientRect();
    window.scrollTo(0, rect.top + window.scrollY - 140);
}

function goToYourRequest() { 
    el = document.getElementById("_yourRequest");
    var rect = el.getBoundingClientRect();
    window.scrollTo(0, rect.top + window.scrollY - 140);
}

function goToRequestedBooks() { 
    el = document.getElementById("_requestedBooks");
    var rect = el.getBoundingClientRect();
    window.scrollTo(0, rect.top + window.scrollY - 140);
}
