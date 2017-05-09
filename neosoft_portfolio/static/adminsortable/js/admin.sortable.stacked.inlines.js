(function($){

    $(function() {
        var sorting_urls = $(':hidden[name="admin_sorting_url"]');
        if (sorting_urls.length > 0)
        {
            var sortable_inline_groups = sorting_urls.closest('.inline-group')
            var sortable_inline_rows = sortable_inline_groups.find('.inline-related');

            sortable_inline_groups.addClass('sortable')
            sortable_inline_rows.addClass('sortable');

            sortable_inline_groups.sortable({
                axis : 'y',
                containment : 'parent',
                create: function(event, ui) {
                    $('.inline-related :checkbox').unbind();
                },
                tolerance : 'pointer',
                items : '.inline-related',
                stop : function(event, ui)
                {
                    if ($('.inline-deletelink').length > 0) {
                        $(ui.sender).sortable('cancel');
                        alert($('#localized_save_before_reorder_message').val());
                        return false;
                    }

                    var indexes = [];
                    ui.item.parent().children('.inline-related').each(function(i)
                    {
                        var index_value = $(this).find(':hidden[name$="-id"]').val();
                        if (index_value !== "" && index_value !== undefined) {
                            indexes.push(index_value);
                        }
                    });

                    $.ajax({
                        url: ui.item.parent().find(':hidden[name="admin_sorting_url"]').val(),
                        type: 'POST',
                        data: { indexes : indexes.join(',') },
                        success: function() {
                            var fieldsets = ui.item.find('fieldset'),
                                highlightedSelector = fieldsets.filter('.collapsed').length === fieldsets.length ? 'h3' : '.form-row',
                                icons = ui.item.parent().find('h3 > .fa');

                            // set icons based on position
                            icons.removeClass('fa-sort-desc fa-sort-asc fa-sort');
                            icons.each(function(index, element) {
                                var icon = $(element);
                                if (index === 0) {
                                    icon.addClass('fa fa-sort-desc');
                                }
                                else if (index == icons.length - 1) {
                                    icon.addClass('fa fa-sort-asc');
                                }
                                else  {
                                    icon.addClass('fa fa-sort');
                                }
                            });

                            ui.item.find(highlightedSelector).effect('highlight', {}, 1000);
                        }
                    });
                }
            });
        }
    });

})(django.jQuery);
