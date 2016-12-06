/**
 * Created by eason on 16-11-20.
 */
var type_names, role_names, storagesites, laboratories;

$(function () {
    $(function () {
        $('#myTab a:first').tab('show');//初始化显示哪个tab
        $('#myTab a').click(function (e) {
          e.preventDefault();//阻止a链接的跳转行为
          $(this).tab('show');//显示当前选中的链接及关联的content
        })
    });
});

function get_error_msg(resp) {
    var msg_json = eval("("+resp.responseText+")");
    var msg = msg_json.detail.msg;
    return msg;
}
function show_change_success() {
    toastr.success('', '修改成功');
}
function show_retuen_success() {
    toastr.success('', '归还成功');
}