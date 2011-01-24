$(function(){

    // bind navigation click events to section containers
    $('#body-links').find('li').click(function(){ 

        $('#body-links').find('a').removeClass('active');
        $(this).find('a').addClass('active');
        $('#body_container').find('.container').hide();
        var show_container = $('#body_container').find('#' + $(this).attr('ref'));
        show_container.show();
        if (show_container.is(':empty'))
            show_container.trigger('refresh');
        
    }).end().find('li:first').click();
    
    // refresh events (load content via ajax)
    $('#overview').bind('refresh', function(){
        $(this).html('<div style="padding:30px;">loading your data from myGengo....</div>').load('/overview');
    });
    
     $('#order').bind('refresh', function(){
        $(this).html('loading...').load('/order');
 
    });
    
    
    $('.nav-details').find('a').live('click', function(){
        var $isActive = $(this).hasClass('active');
            
        var $job = $(this).parents('.job:first');
        $job.find('.nav-details').find('a').removeClass('active');
        $job.find('.details_container').hide(0);
        if ($isActive) return;
        $(this).addClass('active');
        $job.find('#' + $(this).attr('ref')).show(200);
    });
    
    // post a comment 
    $('.save_comment').live('click',function(){
        var $commentForm = $(this).parents('.add_comment');
        var $job = $(this).parents('.job:first');
        var $comments = $job.find('#comments:first');
        var $commentVal = $commentForm.find('textarea').val();
        var $thisButton = $(this);
        $thisButton.attr('disabled',true);
        $.ajax({
                url: '/comment/' + $job.attr('id'),
                type: 'POST',
                data: {
                    "comment": $commentVal,
                    },
                success: function(data) {
                   $commentForm.find('textarea').val(''); 
                   $thisButton.attr('disabled',false);
                   var $newComment = '<div class="comment" style="margin: 10px; padding: 10px;"><i>';
                   $newComment += $commentVal;
                   $newComment += '</i><div style="font-size:.8em;font-style:italic;">by <b>customer</b>  | just now</div></div>';
                   $comments.append($newComment);
                }
            });
        
        
    });
    
    
    
     // post a rating
    $('.submit_rating').live('click',function(){
        var $reviewForm = $(this).parents('#review');
        var $job = $(this).parents('.job:first');
        var $ratingVal = $reviewForm.find('input:checked').val();
        if (!$ratingVal) return alert('you must select a rating!');
        var $thisButton = $(this);
        $thisButton.attr('disabled',true);
        $.ajax({
                url: '/review/' + $job.attr('id'),
                type: 'POST',
                data: {
                    "rating": $ratingVal,
                    },
                success: function(data) {
                   $reviewForm.html('your review has been posted.');
                }
            });
        
        
    });
    


});
