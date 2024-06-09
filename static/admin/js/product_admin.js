// code to render dynamic subcategories based on the selected category in the admin panel
(function ($) {
    $(document).ready(function () {
        const categoryField = $("#id_category");
        const subcategoryField = $("#id_subcategory");

        function updateSubcategories() {
            const selectedCategoryId = categoryField.val();

            $.ajax({
                url: `/api/v1/subcategory?category=${selectedCategoryId}`,
                method: 'GET',
                dataType: 'json',
                success: function (data) {
                    subcategoryField.html('<option value="">---------</option>');
                    $.each(data, function (key, value) {
                        subcategoryField.append($('<option></option>').attr('value', key).text(value.name));
                    });
                }
            });
        }

        // Initial update based on the selected category on page load
        updateSubcategories();

        // Update subcategories when the category field changes
        categoryField.change(updateSubcategories);
    });
})(django.jQuery);
