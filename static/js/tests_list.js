$(function(){

    // init :: begin

    var test_layout =
        '{{if type=="main"}}' +
            '<tr class="filtered-test-row" test_id="${id}">' +
                '<td>' +
                  '<a data-toggle="tooltip" class="change-test" href="${update}" data-original-title="' + gettext('Update') + '">' +
                    '<i class="icon-wrench"></i>' +
                  '</a>' +
                  '<a data-toggle="tooltip" class="remove-test cursor-hand" data-original-title="' + gettext('Remove') + '">' +
                    '<i class="icon-trash"></i>' +
                  '</a>' +
                '</td>' +
                '<td>' +
                  '<a class="filtered-test-id" href="${update}">' +
                    '${doc} (#${id}) ' +
                    '{{if status == "new"}}<small class="muted">[' + gettext('in development') + ']</small>{{/if}}' +
                  '</a>' +
                '</td>' +
                '<td class="filtered-test-url">' +
                    '<a href="${url}" target="_blank">${url}</a>' +
                '</td>' +
                '<td>' +
                    '<div class="tag-list">' +
                        '<div class="tags"></div>' +
                    '</div>' +
                '</td>' +
                '<td>&nbsp;</td>' +
                '<td>${whose}</td>' +
            '</tr>' +
        '{{else}}' +
            '<tr class="filtered-test-row" test_id="${id}">' +
                '<td>' +
                    '<a data-toggle="tooltip" class="change-test" href="${update}" data-original-title="' + gettext('Update') + '">' +
                        '<i class="icon-wrench"></i>' +
                    '</a>' +
                    '<a data-toggle="tooltip" class="remove-test cursor-hand" data-original-title="' + gettext('Remove') + '">' +
                        '<i class="icon-trash"></i>' +
                    '</a>' +
                '</td>' +
                '<td>' +
                    '↳ <a class="filtered-test-id" href="${update}">${doc}(#${id})</a> ' +
                    '{{if status == "new"}}<small class="muted">[' + gettext('in development') + ']</small>{{/if}}' +
                '</td>' +
                '<td>&nbsp;</td>' +
                '<td>' +
                    '<div class="tag-list">' +
                        '<div class="tags"></div>' +
                    '</div>' +
                '</td>' +
                '<td>${parent}</td>' +
                '<td>${whose}</td>' +
            '</tr>' +
        '{{/if}}';

    $.template( "test_layout", test_layout );

    var provider = new gany.dataprovider.DataProvider( tests_data );
    var table = new gany.dataprovider.Table( $( "#tests-list" ), provider );
    $(provider).trigger( "data-changed" );

    var filter_func = function() {
        provider.pagination.page = 1;
        var filters = [];
        $(".like-filter").each( function( ind, el ) {
            filters.push( new gany.dataprovider.LikeFilter( $(el).attr("data-key"), $(el).val() ) );
        } );
        $(".parent-filter").each( function( ind, el ) {
            filters.push( new gany.dataprovider.ParentFilter( $(el).attr("data-key"), $(el).val() ) );
        } );
        $(".tag-filter").each( function( ind, el ) {
            filters.push( new gany.dataprovider.TagFilter( $(el).attr("data-key"), $(el).tags().getTags() ) );
        } );
        provider.filters = filters;
        $(provider).trigger( "data-changed" );
    };

    $(".like-filter").change( filter_func );
    $(".parent-filter").change( filter_func );
    $(".tag-filter").tags({
        promptText : gettext( "Enter tags..." ),
        afterAddingTag : filter_func,
        afterDeletingTag : filter_func
    });

    var pagination_ui = gany.dataprovider.Pagination( $("#pagi-prev"), $("#pagi-next"), $("#page-no"), provider );

    $("#tests-list").delegate( ".remove-test", "click", function() {
        var that = $(this);
        var test_id = $(this).parents("tr,li").attr("test_id");
        gany.modals.rusure( gettext('Are you sure want to remove test') + " " + test_id + " ?", function() {
            this.modal('hide');
            $.post("/test/remove", { test_id : test_id }, function(data) {
                if (data.status == "ok") {
                    for (x in provider.data) {
                        if (provider.data[ x ].id == test_id) {
                            delete provider.data[ x ];
                        }
                    }
                    $(provider).trigger("data-changed");
                } else {
                    gany.modals.error(gettext('Error occured') + ": " + data.content);
                }
            });
        });
    });

});