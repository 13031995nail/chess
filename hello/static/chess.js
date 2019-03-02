// функция запускается когда весь документ полностью загружен
var map;
var divSquare = '<div id="s$coord" class="square $color"></div>';
var divFigure = '<div id="f$coord" class="figure">$figure</div>';
var arr = ['a','b','c','d','e','f','g','h'];
var doska;

$(function(){
	doska = $('#doska').text();
    start();
});

function start(){
    map = new Array(64);
    addSquares();
    ShowBoard(doska);
}

function SetDragSymbol(){
    // draggable позволяет перетаскивать элементы по заданному селектору
    $('.figure').draggable();
}

function SetDropSymbol(){
    /* С помощью метода droppable можно определить область для
       приема перетаскиваемых элементов.
       drop - Определяет функцию, код которой будет выполнен,
       когда перетаскиваемый элемент будет перетащен на принимающую его область (
       при отпуске мыши).
    */
    $('.square').droppable({
        drop: function (event, ui){
            var frCoord = ui.draggable.attr('id').substring(1);
            var toCoord = this.id.substring(1);
            moveFigure(frCoord, toCoord);
			progress(frCoord, toCoord);
           }
        });
}

function moveFigure(frCoord, toCoord){
    console.log('от '+ frCoord + ' k ' + toCoord);
    figure = map[frCoord];
    showFigure(frCoord, '1');
    showFigure(toCoord, figure);
    SetDragSymbol();
}

function addSquares (){
  // очищает содеожимое board
   $('.board').html('');
   // добавление div к board
   // $('.board').append('<div class="square white"></div>');

   // Метод replace осуществляет поиск и замену частей строки.
   // Первым параметром принимается подстрока, которую заменяем, а вторым - подстрока, на которую заменяем.
   for(var coord = 0; coord < 64; coord++)
       $('.board').append(divSquare
                            .replace('$coord',coord)
                            .replace('$color',
                                    isBlackSquare(coord) ? 'black' : 'white'));
   SetDropSymbol();
}

function ShowBoard(figures){
    for(var coord = 0; coord < 64; coord++)
        showFigure(coord, figures.charAt(coord));
}


function showFigure(coord, figure){
    map[coord] = figure;
    $('#s' + coord).html(divFigure
        .replace('$coord', coord)
        .replace('$figure', getChessSymbol(figure)));
    SetDragSymbol();
}

function getChessSymbol(figure){
    /*
     &#9812; - символ короля (белые)   &#9818; - символ короля (черные)
     &#9813; - символ королевы (белые) &#9819; - символ королевы (черные)
     &#9814; - символ ладьи (белые)    &#9820; - символ ладьи (черные)
     &#9815; - символ слона (белые)    &#9821; - символ слона (черные)
     &#9816; - символ коня (белые)     &#9822; - символ коня (черные)
     &#9817; - символ пешки (белые)    &#9823; - символ пешки (черные)
    */
    switch(figure){
        case 'K' : return '&#9812;';
        case 'Q' : return '&#9813;';
        case 'R' : return '&#9814;';
        case 'B' : return '&#9815;';
        case 'N' : return '&#9816;';
        case 'P' : return '&#9817;';
        case 'k' : return '&#9818;';
        case 'q' : return '&#9819;';
        case 'r' : return '&#9820;';
        case 'b' : return '&#9821;';
        case 'n' : return '&#9822;';
        case 'p' : return '&#9823;';
        default : return '';
    }
}

function isBlackSquare(coord){
    return (coord % 8 + Math.floor(coord/8)) % 2
}

function progress(position1, position2){
////end = arr[position2%8]+(8-(Math.floor(position2/8)));
//$.ajax({
//    type: "POST",
//    url: 'test',
//    data:{nail:end}
//});
	//document.location.href = "https://hidden-harbor-40615.herokuapp.com/" + end;
}
function start_game(){
    $.ajax({
	    type: "POST",
		url: 'test',
		success: function(data){
					number = data.indexOf('<div id="doska" style="display:none">');
					data = data.stringOne.slice(number+37, number+101);
					console.log(typeof(data));
				}
	});
	//document.location.href = "https://hidden-harbor-40615.herokuapp.com/start";
}