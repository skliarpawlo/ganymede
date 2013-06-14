$( function() {

    $("#modules-list").delegate( ".remove-module", "click", function() {
        var that = $(this);
        var module_id = $(this).parents("tr,li").attr("module_id");
        gany.modals.rusure( gettext('Are you sure want to remove module') + " " + module_id + " ?", function() {
            this.modal('hide');
            $.post("/modules/remove", { module_id : module_id }, function(data) {
                if (data.status == "ok") {
                    that.parents("tr,li").remove();
                } else {
                    gany.modals.error(gettext('Error occured') + ": " + data.content);
                }
            });
        });
    });

} );
