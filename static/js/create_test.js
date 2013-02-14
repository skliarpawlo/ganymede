$(function(){

    $("#сreate-test-btn").click(function() {
        var data = gany.test.gather_data();
        $.post("", data).done(function(data) {
            if (data.status == "ok") {
                gany.modals.info("Тест успешно добавлен");
            } else {
                gany.modals.error("Возникла ошибка:" + data.content);
            }
        });
    });

});