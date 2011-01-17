function updateQuote(){

    if( $(this).val().length == 0) {
            // Hide the q-suggestions box
            $('#price_quote').text('0.00');
            $('#word_count_quote').text('0');
        } else {
            $('#updating_quote').show();

            $.ajax({
                url: '/service_quote/',
                data: "json",
                type: "POST",
                data: {
                    "body": $('#body_src').val(),
                    "lc_src": $('#lc_src').val(),
                    "lc_tgt": $('#lc_tgt').val(),
                    "tier": $('#tiers').find('input:checked').val(),
                    },
                success: function(data) {
                    $('#updating_quote').hide();
                    if (data.err){
                        $('#price_quote').html(' &nbsp; <i>' + data.err.msg + '</i>');
                        $('#submit_order').attr('disabled',true);
                        return;
                    }
                     $('#submit_order').attr('disabled',false);
                     $('#price_quote').text(data.credits);
                    $('#word_count_quote').text(data.unit_count);
                }
            });
      }

}

$(function(){
    $('#body_src').live('keyup', $.debounce(200, updateQuote));
    $('#lc_src').live('change',updateQuote);
    $('#lc_tgt').live('change',updateQuote);
});
