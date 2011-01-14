function updateQuote(){

    if( $(this).val().length == 0) {
            // Hide the q-suggestions box
            $('#price_quote').text('0.00');
            $('#word_count_quote').text('0');
        } else {
            //$('#price_quote').text('loading...');

            $.ajax({
                url: '/service_quote/',
                data: {
                    "body": $('#body_src').val(),
                    "lc_src": $('#lc_src').val(),
                    "lc_tgt": $('#lc_tgt').val(),
                    "tier": $('#tiers').find('input:checked').val(),
                    },
                success: function(data) {
                    $('#price_quote').text(data);
                }
            });
      }

}

$(function(){
    $('#body_src').live('keyup', $.debounce(200, updateQuote));
    $('#lc_src').live('change',updateQuote);
    $('#lc_tgt').live('change',updateQuote);
});
