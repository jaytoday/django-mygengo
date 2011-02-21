$(function(){

    function getJob(joblink){
        var job_id = joblink.attr('id');
        var job_container = $('<div class="job_container">loading...</div>');
        joblink.append(job_container);

        $.ajax({
        url: '/job/' + job_id,
        type: 'POST',
        dataType: 'html', 
        data: {},
        success: function(data) {
           job_container.html(data);
        },
        error: function(){
            job_container.text('there was an error while completing this action.');
        },
        complete: function(){
            $(document).trigger('jobs_init');
        }
    });

    };
            
    // load jobs 
    $(document).bind('jobs_init', function(){
        $('.job_link').each(function(){
            if ($('#job_container').find('#' + $(this).attr('id')).length < 1)
                $(this).show();
        });
    });
    $('.job_link').find('a.shortcut').live('click',function(){ 
        var $joblink = $(this).parents('.job_link:first');
        if ($(this).hasClass('clicked')) 
            return $joblink.find('.job_container').toggle('fast');
        else
            $(this).addClass('clicked');
        
            getJob($joblink);            
    });
    
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
    
     // post purchase
     $('#submit_purchase').live('click',function(){
        var $reviewForm = $(this).parents('#purchase');
        var $job = $(this).parents('.job:first');
        var $thisButton = $(this);
        $thisButton.attr('disabled',true);
        $.ajax({
                url: '/purchase/' + $job.attr('id'),
                type: 'POST',
                data: {},
                success: function(data) {
                   $reviewForm.html('your purchase has been saved.');
                },
                complete: function() {
                    getJob($reviewForm.parents('.job:first').attr('id'));
                }
            });

    });  
        
    
     // post approval
    $('#submit_approve').live('click',function(){
        var $reviewForm = $(this).parents('#approve');
        var $job = $(this).parents('.job:first');
        var $ratingVal = $reviewForm.find('.ratings').find('input:checked').val();
        if (!$ratingVal) return alert('you must select a rating!');
        var $thisButton = $(this);
        $thisButton.attr('disabled',true);
        var $approvalData = {
                    "rating": $ratingVal,
                    "for_translator": $reviewForm.find('#for_translator').val(),
                    "for_mygengo": $reviewForm.find('#for_mygengo').val(),
         }
         if ($reviewForm.find('#public:checked').length > 0)
            $approvalData['public'] = 1;
         else 
            $approvalData['public'] = 0;      
        $.ajax({
                url: '/approve/' + $job.attr('id'),
                type: 'POST',
                data: $approvalData,
                success: function(data) {
                   $reviewForm.html('your approval has been saved.');
                },
                complete: function() {
                    getJob($reviewForm.parents('.job:first').attr('id'));
                }
            });
        
        
    });
    
    
     // post revision request
     $('#submit_revise').live('click',function(){
        var $reviewForm = $(this).parents('#revise');
        var $job = $(this).parents('.job:first');
        var $comment = $reviewForm.find('#revise_comment').val();
        if (!$comment) return alert('you must provide a comment!');
        var $thisButton = $(this);
        $thisButton.attr('disabled',true);
        $.ajax({
                url: '/revise/' + $job.attr('id'),
                type: 'POST',
                data: {
                    "comment": $comment,
                    },
                success: function(data) {
                   $reviewForm.html('your request has been sent.');
                },
                complete: function() {
                    getJob($reviewForm.parents('.job:first').attr('id'));
                }
            });

    });   
    
 
     // post rejection
     $('#submit_reject').live('click',function(){
        var $reviewForm = $(this).parents('#reject');
        var $job = $(this).parents('.job:first');
        var $reason = $reviewForm.find('#reason').val();
        if (!$reason) return alert('you must provide a reason!');        
        var $comment = $reviewForm.find('#reject_comment').val();
        if (!$comment) return alert('you must provide a comment!');
        var $captcha = $reviewForm.find('#captcha').val();
        if (!$captcha) return alert('you must provide a captcha text!');        
        if ($reviewForm.find('#follow_up:checked').length > 0)
            var $follow_up = 'requeue';
        else
            var $follow_up = 'cancel';
        if (!$comment) return alert('you must provide a comment!');        
        var $thisButton = $(this);
        $thisButton.attr('disabled',true);
        $.ajax({
                url: '/reject/' + $job.attr('id'),
                type: 'POST',
                data: {
                    "comment": $comment,
                    "reason": $reason,
                    "captcha": $captcha,
                    "follow_up": $follow_up,
                    },
                success: function(data) {
                   $reviewForm.html('your rejection has been sent.');
                },
                complete: function() {
                    getJob($reviewForm.parents('.job:first').attr('id'));
                }
            });

    });     


});
