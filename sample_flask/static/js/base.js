// adain_choose 그림 보여주는 부분
$(document).ready(function(){
    $('.oriental').hide();
    $('.cartoon').hide();
    $('.western').hide();
    $('.popart').hide();
    $('#loading').hide();
});

$("input[id='동양화']").on('click', function() {
    $('.oriental').show();
    $('.cartoon').hide();
    $('.western').hide();
    $('.popart').hide();
    $("input[name='western']").prop('checked', false) 
    $("input[name='cartoon']").prop('checked', false)
    $("input[name='popart']").prop('checked', false)
    
});
$("input[id='만화']").on('click', function() {
    $('.cartoon').show();
    $('.oriental').hide();
    $('.western').hide();
    $('.popart').hide();
    $("input:radio[name='oriental']").prop('checked', false)
    $("input:radio[name='western']").prop('checked', false)    
    $("input:radio[name='popart']").prop('checked', false)
});
$("input[id='서양화']").on('click', function() {
    $('.western').show();
    $('.oriental').hide();
    $('.cartoon').hide();
    $('.popart').hide();
    $("input:radio[name='oriental']").prop('checked', false)
    $("input:radio[name='cartoon']").prop('checked', false)    
    $("input:radio[name='popart']").prop('checked', false)
});
$("input[id='팝아트']").on('click', function() {
    $('.popart').show();
    $('.oriental').hide();
    $('.cartoon').hide();
    $('.western').hide();
    $("input:radio[name='oriental']").prop('checked', false)
    $("input:radio[name='western']").prop('checked', false)
    $("input:radio[name='cartoon']").prop('checked', false)    
});

// form 태그 submit 할 때 스피너
$('#adain_upload').submit(function(){
    $('.adain_design_select').hide();
    $('#loading').show();  
    return true 
});
$('#myHand').submit(function(){
    $('#adain_ment').hide();
    $('#adain_make_div').hide();
    $('#loading').show();  
    return true 
});

$('#myForm').submit(function(){    
    $('#sandle_upload').hide();
    $('#upload_banner').hide();
    $('#loading').show();  
    return true 
});

$('#myHand_weather').submit(function(){
    $('#weather_nail_list').hide();
    $('#loading').show();  
    return true 
});

$('#myFoot_weather').submit(function(){
    $('#weather_pedi_list').hide();
    $('#loading').show();  
    return true 
});

$('#myFoot_sandle').submit(function(){
    $('#sandle_pedi_list').hide();
    $('#loading').show();  
    return true 
});

$('#myHand_select').submit(function(){
    $('#select_nail_list').hide();
    $('#loading').show();  
    return true 
});

$('#myFoot_select').submit(function(){
    $('#select_pedi_list').hide();
    $('#loading').show();  
    return true 
});

$('#myHand_celeb').submit(function(){
    $('#celeb_make').hide();
    $('#loading').show();  
    return true 
});


// 샌들 업로드 됐을 때
$(document).ready(function(){
    $('#pedi_ones').hide();
    $('#pedi_diverse').hide();

    
    if ($("input:radio[id='ones']:checked").length > 0) {
        $('#pedi_ones').css("display", "block");
        $('#pedi_diverse').css("display", "none");
    }

    if ($("input:radio[id='diverse']:checked").length > 0) {
        $('#pedi_ones').hide();
        $('#pedi_diverse').show();
    }
});

$("input:radio[id='ones']").on('click', function() {
    $('#pedi_ones').show();
    $('#pedi_diverse').hide();
    $("input:radio[name='diverse']").prop('checked', false)
});

$("input[id='diverse']").on('click', function() {
    $('#pedi_ones').hide();
    $('#pedi_diverse').show();
    $("input:radio[name='ones']").prop('checked', false)
});

// 클릭 옵션 


// 연예인 사진 선택할 때
$(document).ready(function(){
    $('#rose1').hide();
    $('#rose2').hide();
    $('#rose3').hide();
    $('#rose4').hide();
    $('#minkyeong1').hide();
    $('#minkyeong2').hide();
    $('#minkyeong3').hide();
    $('#minkyeong4').hide();
    $('#joy1').hide();
    $('#joy2').hide();
    $('#joy3').hide();
    $('#joy4').hide();
    $('#hyoyeon1').hide();
    $('#hyoyeon2').hide();
    $('#hyoyeon3').hide();
    $('#hyoyeon4').hide();
});

$("#rose_image_1").on('click', function() {
    $('#rose1').show();
    $('#rose_card1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card1_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card1_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card1_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card1_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose2').hide();
    $('#rose_card2').css('background-color', 'white')
    $('#rose_card2_list1').css('background-color', 'white')
    $('#rose_card2_list2').css('background-color', 'white')
    $('#rose_card2_list3').css('background-color', 'white')
    $('#rose_card2_list4').css('background-color', 'white')
    $('#rose3').hide();
    $('#rose_card3').css('background-color', 'white')
    $('#rose_card3_list1').css('background-color', 'white')
    $('#rose_card3_list2').css('background-color', 'white')
    $('#rose_card3_list3').css('background-color', 'white')
    $('#rose_card3_list4').css('background-color', 'white')
    $('#rose4').hide();
    $('#rose_card4').css('background-color', 'white')
    $('#rose_card4_list1').css('background-color', 'white')
    $('#rose_card4_list2').css('background-color', 'white')
    $('#rose_card4_list3').css('background-color', 'white')
    $('#rose_card4_list4').css('background-color', 'white')
    
});

$("#rose_image_2").on('click', function() {
    $('#rose1').hide();
    $('#rose_card1').css('background-color', 'white')
    $('#rose_card1_list1').css('background-color', 'white')
    $('#rose_card1_list2').css('background-color', 'white')
    $('#rose_card1_list3').css('background-color', 'white')
    $('#rose_card1_list4').css('background-color', 'white')
    $('#rose2').show();
    $('#rose_card2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card2_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card2_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card2_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card2_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose3').hide();
    $('#rose_card3').css('background-color', 'white')
    $('#rose_card3_list1').css('background-color', 'white')
    $('#rose_card3_list2').css('background-color', 'white')
    $('#rose_card3_list3').css('background-color', 'white')
    $('#rose_card3_list4').css('background-color', 'white')
    $('#rose4').hide();
    $('#rose_card4').css('background-color', 'white')
    $('#rose_card4_list1').css('background-color', 'white')
    $('#rose_card4_list2').css('background-color', 'white')
    $('#rose_card4_list3').css('background-color', 'white')
    $('#rose_card4_list4').css('background-color', 'white')
});

$("#rose_image_3").on('click', function() {
    $('#rose1').hide();
    $('#rose_card1').css('background-color', 'white')
    $('#rose_card1_list1').css('background-color', 'white')
    $('#rose_card1_list2').css('background-color', 'white')
    $('#rose_card1_list3').css('background-color', 'white')
    $('#rose_card1_list4').css('background-color', 'white')
    $('#rose2').hide();
    $('#rose_card2').css('background-color', 'white')
    $('#rose_card2_list1').css('background-color', 'white')
    $('#rose_card2_list2').css('background-color', 'white')
    $('#rose_card2_list3').css('background-color', 'white')
    $('#rose_card2_list4').css('background-color', 'white')
    $('#rose3').show();
    $('#rose_card3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card3_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card3_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card3_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card3_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose4').hide();
    $('#rose_card4').css('background-color', 'white')
    $('#rose_card4_list1').css('background-color', 'white')
    $('#rose_card4_list2').css('background-color', 'white')
    $('#rose_card4_list3').css('background-color', 'white')
    $('#rose_card4_list4').css('background-color', 'white')
});

$("#rose_image_4").on('click', function() {
    $('#rose1').hide();
    $('#rose_card1').css('background-color', 'white')
    $('#rose_card1_list1').css('background-color', 'white')
    $('#rose_card1_list2').css('background-color', 'white')
    $('#rose_card1_list3').css('background-color', 'white')
    $('#rose_card1_list4').css('background-color', 'white')
    $('#rose2').hide();
    $('#rose_card2').css('background-color', 'white')
    $('#rose_card2_list1').css('background-color', 'white')
    $('#rose_card2_list2').css('background-color', 'white')
    $('#rose_card2_list3').css('background-color', 'white')
    $('#rose_card2_list4').css('background-color', 'white')
    $('#rose3').hide();
    $('#rose_card3').css('background-color', 'white')
    $('#rose_card3_list1').css('background-color', 'white')
    $('#rose_card3_list2').css('background-color', 'white')
    $('#rose_card3_list3').css('background-color', 'white')
    $('#rose_card3_list4').css('background-color', 'white')
    $('#rose4').show();
    $('#rose_card4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card4_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card4_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card4_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#rose_card4_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
});

$("#minkyeong_image_1").on('click', function() {
    $('#minkyeong1').show();
    $('#minkyeong_card1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card1_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card1_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card1_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card1_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong2').hide();
    $('#minkyeong_card2').css('background-color', 'white')
    $('#minkyeong_card2_list1').css('background-color', 'white')
    $('#minkyeong_card2_list2').css('background-color', 'white')
    $('#minkyeong_card2_list3').css('background-color', 'white')
    $('#minkyeong_card2_list4').css('background-color', 'white')
    $('#minkyeong3').hide();
    $('#minkyeong_card3').css('background-color', 'white')
    $('#minkyeong_card3_list1').css('background-color', 'white')
    $('#minkyeong_card3_list2').css('background-color', 'white')
    $('#minkyeong_card3_list3').css('background-color', 'white')
    $('#minkyeong_card3_list4').css('background-color', 'white')
    $('#minkyeong4').hide();
    $('#minkyeong_card4').css('background-color', 'white')
    $('#minkyeong_card4_list1').css('background-color', 'white')
    $('#minkyeong_card4_list2').css('background-color', 'white')
    $('#minkyeong_card4_list3').css('background-color', 'white')
    $('#minkyeong_card4_list4').css('background-color', 'white')
});

$("#minkyeong_image_2").on('click', function() {
    $('#minkyeong1').hide();
    $('#minkyeong_card1').css('background-color', 'white')
    $('#minkyeong_card1_list1').css('background-color', 'white')
    $('#minkyeong_card1_list2').css('background-color', 'white')
    $('#minkyeong_card1_list3').css('background-color', 'white')
    $('#minkyeong_card1_list4').css('background-color', 'white')
    $('#minkyeong2').show();
    $('#minkyeong_card2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card2_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card2_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card2_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card2_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong3').hide();
    $('#minkyeong_card3').css('background-color', 'white')
    $('#minkyeong_card3_list1').css('background-color', 'white')
    $('#minkyeong_card3_list2').css('background-color', 'white')
    $('#minkyeong_card3_list3').css('background-color', 'white')
    $('#minkyeong_card3_list4').css('background-color', 'white')
    $('#minkyeong4').hide();
    $('#minkyeong_card4').css('background-color', 'white')
    $('#minkyeong_card4_list1').css('background-color', 'white')
    $('#minkyeong_card4_list2').css('background-color', 'white')
    $('#minkyeong_card4_list3').css('background-color', 'white')
    $('#minkyeong_card4_list4').css('background-color', 'white')
});

$("#minkyeong_image_3").on('click', function() {
    $('#minkyeong1').hide();
    $('#minkyeong_card1').css('background-color', 'white')
    $('#minkyeong_card1_list1').css('background-color', 'white')
    $('#minkyeong_card1_list2').css('background-color', 'white')
    $('#minkyeong_card1_list3').css('background-color', 'white')
    $('#minkyeong_card1_list4').css('background-color', 'white')
    $('#minkyeong2').hide();
    $('#minkyeong_card2').css('background-color', 'white')
    $('#minkyeong_card2_list1').css('background-color', 'white')
    $('#minkyeong_card2_list2').css('background-color', 'white')
    $('#minkyeong_card2_list3').css('background-color', 'white')
    $('#minkyeong_card2_list4').css('background-color', 'white')
    $('#minkyeong3').show();
    $('#minkyeong_card3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card3_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card3_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card3_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card3_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong4').hide();
    $('#minkyeong_card4').css('background-color', 'white')
    $('#minkyeong_card4_list1').css('background-color', 'white')
    $('#minkyeong_card4_list2').css('background-color', 'white')
    $('#minkyeong_card4_list3').css('background-color', 'white')
    $('#minkyeong_card4_list4').css('background-color', 'white')
});

$("#minkyeong_image_4").on('click', function() {
    $('#minkyeong1').hide();
    $('#minkyeong_card1').css('background-color', 'white')
    $('#minkyeong_card1_list1').css('background-color', 'white')
    $('#minkyeong_card1_list2').css('background-color', 'white')
    $('#minkyeong_card1_list3').css('background-color', 'white')
    $('#minkyeong_card1_list4').css('background-color', 'white')
    $('#minkyeong2').hide();
    $('#minkyeong_card2').css('background-color', 'white')
    $('#minkyeong_card2_list1').css('background-color', 'white')
    $('#minkyeong_card2_list2').css('background-color', 'white')
    $('#minkyeong_card2_list3').css('background-color', 'white')
    $('#minkyeong_card2_list4').css('background-color', 'white')
    $('#minkyeong3').hide();
    $('#minkyeong_card3').css('background-color', 'white')
    $('#minkyeong_card3_list1').css('background-color', 'white')
    $('#minkyeong_card3_list2').css('background-color', 'white')
    $('#minkyeong_card3_list3').css('background-color', 'white')
    $('#minkyeong_card3_list4').css('background-color', 'white')
    $('#minkyeong4').show();
    $('#minkyeong_card4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card4_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card4_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card4_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#minkyeong_card4_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
});

$("#joy_image_1").on('click', function() {
    $('#joy1').show();
    $('#joy_card1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card1_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card1_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card1_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card1_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy2').hide();
    $('#joy_card2').css('background-color', 'white')
    $('#joy_card2_list1').css('background-color', 'white')
    $('#joy_card2_list2').css('background-color', 'white')
    $('#joy_card2_list3').css('background-color', 'white')
    $('#joy_card2_list4').css('background-color', 'white')
    $('#joy3').hide();
    $('#joy_card3').css('background-color', 'white')
    $('#joy_card3_list1').css('background-color', 'white')
    $('#joy_card3_list2').css('background-color', 'white')
    $('#joy_card3_list3').css('background-color', 'white')
    $('#joy_card3_list4').css('background-color', 'white')
    $('#joy4').hide();
    $('#joy_card4').css('background-color', 'white')
    $('#joy_card4_list1').css('background-color', 'white')
    $('#joy_card4_list2').css('background-color', 'white')
    $('#joy_card4_list3').css('background-color', 'white')
    $('#joy_card4_list4').css('background-color', 'white')
});

$("#joy_image_2").on('click', function() {
    $('#joy1').hide();
    $('#joy_card1').css('background-color', 'white')
    $('#joy_card1_list1').css('background-color', 'white')
    $('#joy_card1_list2').css('background-color', 'white')
    $('#joy_card1_list3').css('background-color', 'white')
    $('#joy_card1_list4').css('background-color', 'white')
    $('#joy2').show();
    $('#joy_card2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card2_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card2_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card2_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card2_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy3').hide();
    $('#joy_card3').css('background-color', 'white')
    $('#joy_card3_list1').css('background-color', 'white')
    $('#joy_card3_list2').css('background-color', 'white')
    $('#joy_card3_list3').css('background-color', 'white')
    $('#joy_card3_list4').css('background-color', 'white')
    $('#joy4').hide();
    $('#joy_card4').css('background-color', 'white')
    $('#joy_card4_list1').css('background-color', 'white')
    $('#joy_card4_list2').css('background-color', 'white')
    $('#joy_card4_list3').css('background-color', 'white')
    $('#joy_card4_list4').css('background-color', 'white')
});

$("#joy_image_3").on('click', function() {
    $('#joy1').hide();
    $('#joy_card1').css('background-color', 'white')
    $('#joy_card1_list1').css('background-color', 'white')
    $('#joy_card1_list2').css('background-color', 'white')
    $('#joy_card1_list3').css('background-color', 'white')
    $('#joy_card1_list4').css('background-color', 'white')
    $('#joy2').hide();
    $('#joy_card2').css('background-color', 'white')
    $('#joy_card2_list1').css('background-color', 'white')
    $('#joy_card2_list2').css('background-color', 'white')
    $('#joy_card2_list3').css('background-color', 'white')
    $('#joy_card2_list4').css('background-color', 'white')
    $('#joy3').show();
    $('#joy_card3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card3_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card3_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card3_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card3_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy4').hide();
    $('#joy_card4').css('background-color', 'white')
    $('#joy_card4_list1').css('background-color', 'white')
    $('#joy_card4_list2').css('background-color', 'white')
    $('#joy_card4_list3').css('background-color', 'white')
    $('#joy_card4_list4').css('background-color', 'white')
});

$("#joy_image_4").on('click', function() {
    $('#joy1').hide();
    $('#joy_card1').css('background-color', 'white')
    $('#joy_card1_list1').css('background-color', 'white')
    $('#joy_card1_list2').css('background-color', 'white')
    $('#joy_card1_list3').css('background-color', 'white')
    $('#joy_card1_list4').css('background-color', 'white')
    $('#joy2').hide();
    $('#joy_card2').css('background-color', 'white')
    $('#joy_card2_list1').css('background-color', 'white')
    $('#joy_card2_list2').css('background-color', 'white')
    $('#joy_card2_list3').css('background-color', 'white')
    $('#joy_card2_list4').css('background-color', 'white')
    $('#joy3').hide();
    $('#joy_card3').css('background-color', 'white')
    $('#joy_card3_list1').css('background-color', 'white')
    $('#joy_card3_list2').css('background-color', 'white')
    $('#joy_card3_list3').css('background-color', 'white')
    $('#joy_card3_list4').css('background-color', 'white')
    $('#joy4').show();
    $('#joy_card4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card4_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card4_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card4_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#joy_card4_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
});

$("#hyoyeon_image_1").on('click', function() {
    $('#hyoyeon1').show();
    $('#hyoyeon_card1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card1_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card1_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card1_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card1_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon2').hide();
    $('#hyoyeon_card2').css('background-color', 'white')
    $('#hyoyeon_card2_list1').css('background-color', 'white')
    $('#hyoyeon_card2_list2').css('background-color', 'white')
    $('#hyoyeon_card2_list3').css('background-color', 'white')
    $('#hyoyeon_card2_list4').css('background-color', 'white')
    $('#hyoyeon3').hide();
    $('#hyoyeon_card3').css('background-color', 'white')
    $('#hyoyeon_card3_list1').css('background-color', 'white')
    $('#hyoyeon_card3_list2').css('background-color', 'white')
    $('#hyoyeon_card3_list3').css('background-color', 'white')
    $('#hyoyeon_card3_list4').css('background-color', 'white')
    $('#hyoyeon4').hide();
    $('#hyoyeon_card4').css('background-color', 'white')
    $('#hyoyeon_card4_list1').css('background-color', 'white')
    $('#hyoyeon_card4_list2').css('background-color', 'white')
    $('#hyoyeon_card4_list3').css('background-color', 'white')
    $('#hyoyeon_card4_list4').css('background-color', 'white')
});

$("#hyoyeon_image_2").on('click', function() {
    $('#hyoyeon1').hide();
    $('#hyoyeon_card1').css('background-color', 'white')
    $('#hyoyeon_card1_list1').css('background-color', 'white')
    $('#hyoyeon_card1_list2').css('background-color', 'white')
    $('#hyoyeon_card1_list3').css('background-color', 'white')
    $('#hyoyeon_card1_list4').css('background-color', 'white')
    $('#hyoyeon2').show();
    $('#hyoyeon_card2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card2_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card2_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card2_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card2_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon3').hide();
    $('#hyoyeon_card3').css('background-color', 'white')
    $('#hyoyeon_card3_list1').css('background-color', 'white')
    $('#hyoyeon_card3_list2').css('background-color', 'white')
    $('#hyoyeon_card3_list3').css('background-color', 'white')
    $('#hyoyeon_card3_list4').css('background-color', 'white')
    $('#hyoyeon4').hide();
    $('#hyoyeon_card4').css('background-color', 'white')
    $('#hyoyeon_card4_list1').css('background-color', 'white')
    $('#hyoyeon_card4_list2').css('background-color', 'white')
    $('#hyoyeon_card4_list3').css('background-color', 'white')
    $('#hyoyeon_card4_list4').css('background-color', 'white')
});

$("#hyoyeon_image_3").on('click', function() {
    $('#hyoyeon1').hide();
    $('#hyoyeon_card1').css('background-color', 'white')
    $('#hyoyeon_card1_list1').css('background-color', 'white')
    $('#hyoyeon_card1_list2').css('background-color', 'white')
    $('#hyoyeon_card1_list3').css('background-color', 'white')
    $('#hyoyeon_card1_list4').css('background-color', 'white')
    $('#hyoyeon2').hide();
    $('#hyoyeon_card2').css('background-color', 'white')
    $('#hyoyeon_card2_list1').css('background-color', 'white')
    $('#hyoyeon_card2_list2').css('background-color', 'white')
    $('#hyoyeon_card2_list3').css('background-color', 'white')
    $('#hyoyeon_card2_list4').css('background-color', 'white')
    $('#hyoyeon3').show();
    $('#hyoyeon_card3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card3_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card3_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card3_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card3_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon4').hide();
    $('#hyoyeon_card4').css('background-color', 'white')
    $('#hyoyeon_card4_list1').css('background-color', 'white')
    $('#hyoyeon_card4_list2').css('background-color', 'white')
    $('#hyoyeon_card4_list3').css('background-color', 'white')
    $('#hyoyeon_card4_list4').css('background-color', 'white')
});

$("#hyoyeon_image_4").on('click', function() {
    $('#hyoyeon1').hide();
    $('#hyoyeon_card1').css('background-color', 'white')
    $('#hyoyeon_card1_list1').css('background-color', 'white')
    $('#hyoyeon_card1_list2').css('background-color', 'white')
    $('#hyoyeon_card1_list3').css('background-color', 'white')
    $('#hyoyeon_card1_list4').css('background-color', 'white')
    $('#hyoyeon2').hide();
    $('#hyoyeon_card2').css('background-color', 'white')
    $('#hyoyeon_card2_list1').css('background-color', 'white')
    $('#hyoyeon_card2_list2').css('background-color', 'white')
    $('#hyoyeon_card2_list3').css('background-color', 'white')
    $('#hyoyeon_card2_list4').css('background-color', 'white')
    $('#hyoyeon3').hide();
    $('#hyoyeon_card3').css('background-color', 'white')
    $('#hyoyeon_card3_list1').css('background-color', 'white')
    $('#hyoyeon_card3_list2').css('background-color', 'white')
    $('#hyoyeon_card3_list3').css('background-color', 'white')
    $('#hyoyeon_card3_list4').css('background-color', 'white')
    $('#hyoyeon4').show();
    $('#hyoyeon_card4').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card4_list1').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card4_list2').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card4_list3').css('background-color', 'rgba(255, 215, 222, 0.747)')
    $('#hyoyeon_card4_list4').css('background-color', 'rgba(255, 215, 222, 0.747)')
});