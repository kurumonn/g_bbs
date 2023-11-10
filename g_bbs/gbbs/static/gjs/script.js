window.addEventListener("load", function () {

    //イベントをセットする要素が動的に変化する場合、documentからイベントを指定する
    $(document).on("click", "#submit_form", function () {
        submit_form();
    });
    $(document).on("click", ".trash", function () {
        trash(this);
    });

    refresh();
});

function submit_form() {

    let form_elem = "#form_area";

    let data = new FormData($(form_elem).get(0));
    let url = $(form_elem).prop("action");
    let method = $(form_elem).prop("method");

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done(function (data, status, xhr) {

        if (data && data.error) {
            console.log("ERROR");
            console.log("Request failed with status: " + status);
            console.log("Error message: " + data.error);
        } else {
            $("#content_area").html(data.content);
            $("#textarea").val("");
        }

    }).fail(function (xhr, status, error) {
        console.log(status + ":" + error);
    }).always(function () {

        //成功しても失敗しても実行されるalways
        console.log("refresh");

        //ロングポーリング(サーバー内で回すよう)に仕立てるので、リクエストの送信はほぼ即時で問題ない
        setTimeout(refresh, 500);

    });
}

function refresh() {
    // リフレッシュの処理を記述する
    console.log("Refreshing...");
    // ここにリフレッシュの具体的な処理を追加してください
}

window.refresh = refresh; // 追加

refresh(); // 追加