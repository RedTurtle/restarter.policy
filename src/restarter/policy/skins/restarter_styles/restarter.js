jQuery(document).ready(function() {
//    jq('#companyStoriesList div a').popover({trigger:'hover', title: 'More information', content: 'More information about this story...'})

    /**** facce in home ***/
    jq("#faFacce div.unaFaccia").hover(function(event) {
        jq(this).popover({trigger:'hover', title: false, position: 'right', classes: 'popoverFacciaDetail', content: $(this).children('.facciaPreview') });
    });

    /*** other products ****/
    jq('#other-products-portlet').parent().insertAfter($('#portal-logo'));
    jq('#other-products-portlet').show();

    jq("#other-products-portlet div.productMiniPreview").hover(function(event) {
        jq(this).popover({trigger:'hover', title: false, position: 'right', classes: 'popoverProductDetail', content: $(this).siblings('.productDetailPreview') });
    });
});