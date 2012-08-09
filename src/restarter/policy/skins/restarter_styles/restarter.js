jQuery(document).ready(function() {
    jq('#companyStoriesList div a').popover({trigger:'hover', title: 'More information', content: 'More information about this story...'})
    jq('#other-products-portlet').parent().insertAfter($('#portal-logo'));
    jq('#other-products-portlet').show();
});
