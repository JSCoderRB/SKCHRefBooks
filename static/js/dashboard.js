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

function goTo(el,speed) {
    var rect = el.getBoundingClientRect();
    x = window.scrollY;
    inc = 1;
    pos = rect.top + window.scrollY - 140;
    if(x > pos){
        inc = -1;
    }
    function scroll(){
        console.log(x, pos, Math.abs(pos - x), speed*inc, Math.abs(pos - x) > speed*inc);
        window.scrollTo(0, x);
        if(Math.abs(pos - x) > Math.abs(speed*inc)) {
            x += speed*inc;
            window.requestAnimationFrame(scroll);
        }else{
            window.scrollTo(0,pos);
        }
    }
    scroll();
}

function goToAvailableBooks() {
    el = document.getElementById("_availableBooks");
    goTo(el, 50);
}

function goToUploadedBooks() {
    el = document.getElementById("_uploadedBooks");
    goTo(el, 50);
}

function goToYourRequest() {
    el = document.getElementById("_yourRequest");
    goTo(el, 50);
}

function goToRequestedBooks() {
    el = document.getElementById("_requestedBooks");
    goTo(el, 50);
}
