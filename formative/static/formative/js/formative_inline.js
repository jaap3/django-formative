// namespace in the global scope
var formative = {};


(function ($) {


    formative.selectType = function (e) {
        // Handle OK button click, figure out form prefix and selected type.
        e.preventDefault();
        var $select = $('select', $(this).parent()),
            formative_type = $select.val(),
            prefix = $select.attr('name').split('-formative_type')[0];
        $select.prop('disabled', true);
        $(this).prop('disabled', true);
        formative.getForm(
            $(this).parents('.field-formative_type').parent(),
            formative_type, prefix);
    };


    formative.getForm = function ($container, formative_type, prefix) {
        // Replace the type select form with the actual form
        var data ={
            formative_type: formative_type,
            prefix: prefix
        };
        $.get('../formative_form', data, function (response) {
            $form = $(response.trim());
            $form.insertAfter($container);
            formative.addOkButton($form);
            $container.remove();
        });
    };


    formative.addOkButton = function ($container) {
        var selectButton = $('<input type="button" value="OK">');
        selectButton.click(formative.selectType);
        selectButton.insertAfter($('.field-formative_type select', $container));
    };

    $(function () {
        formative.addOkButton($('.inline-group'));
    });


}(django.jQuery));
