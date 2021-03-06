/**
 * Created by eason on 16-11-14.
 */
var types, users ,approves;

$(function () {

    // register
    $('#reg').click(function () {
       $('#registerModal').modal('toggle');
    });
    $('#add-user-btn').click(function () {
       $('#addUserModal').modal('toggle');
    });
    $('#add-storagesites-btn').click(function () {
       $('#addStorageSitesModal').modal('toggle');
    });
    $('#add-laboratories-btn').click(function () {
       $('#addLaboratoriesModal').modal('toggle');
    });
    $('#add-approves-btn').click(function () {
        create_users_select();
       $('#addApproveModal').modal('toggle');
    });
    $('#register-btn').click(function () {
        register();
    });
    //login
    $('#login-btn').click(function () {
        login();

    });
    //get_organization_data
    $('#get-organization-btn').click(function () {
        get_organization_data();
    });
    $('#save').click(function () {
        save_orgnization();
    });
    $('#get-users-btn').click(function () {
        get_users()
    });
    $('#add-member-btn').click(function () {

        $.ajax({
            url: '/api/v1/admin/users/',
            data: $('#add-user-form').serialize(),
            headers:{
                Authorization: $.cookie("token")
            },
            type: 'POST',
            dataType: "json",
            success: function (resp) {
                $('#addUserModal').modal('hide');
                $.each(resp, function (index, item) {

                });
            },
            error: function () {

            }
        });
    });
    $('#get-storagesites-btn').click(function () {
        get_storagesites();
    });
    $('#add-storagesite-btn').click(function () {
        add_storagesite();
    });
    $('#get-laboratory-btn').click(function () {
        get_laboratories();
    });
    $('#add-laboratory-btn').click(function () {
        add_laboratories();
    });
    $('#add-approve-btn').click(function () {
       add_approves();
    });
    get_organization_type_name('#organization-type');
    // get_role_name();
    get_users();
    get_laboratories();
    get_storagesites();
    get_organization_data();
    get_approves();
    get_organization_type_name('#type');


    console.log(storagesites);
});
function get_organization_type_name(id) {
    $.ajax({
        url: '/api/v1/admin/organizations/type_name/',
        type: 'GET',
        dataType: "json",
        success: function (resp) {
            types = resp;
            $.each(resp, function (index, item) {
                $(id).append("<option value="+index+">"+item+"</option>");
            });
        },
        error: function () {
        }
    });
}

function register() {
    $.ajax({
        url: '/api/v1/admin/register/',
        data: $('#register-form').serialize(),
        dataType: "json",
        type: 'POST',
        success: function () {

        },
        error: function (resp, status, err) {
            //console.log(resp.responseText);
            var msg = eval("("+resp.responseText+")");
            //console.log(msg.detail);
            error_msg = msg.detail;
            $('.input-area').children("div:last-child").html('');
            $.each(error_msg, function (key, value) {
                if(key=='non_field_errors'){
                    $('#password2').html(value);
                }
                $('#'+key).html(value);
            });
        }
    });
}

function login() {
    $.ajax({
        url: '/api/v1/admin/auths/login/',
        data: $('#login-form').serialize(),
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            var token = resp.token
            document.cookie="token="+token;
            $('#token').val(token);
            window.location.href = '/index';
        },
        error: function () {
        }
    });

}
// organization
function get_organization_data() {
    $.ajax({
        async: false,
        url: '/api/v1/admin/organizations/',
        headers:{
               Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            var organization = resp.results[0];
            $('#organization-id').val(organization.id);
            $.each(organization, function (key, value) {
                var id = '#' + key;
                $(id).val(value);
            });
        },
        error: function () {

        }

    });
}
function save_orgnization() {
    $.ajax({
        url: '/api/v1/admin/organizations/' + $('#organization-id').val() + '/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#organization-form').serialize(),
        dataType: 'json',
        type: 'PATCH',
        success: function (resp) {
            show_change_success();
        },
        error: function () {
            toastr.error('', '请输入完整信息');

           }

    });
}

// users
function get_users(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        url: '/api/v1/admin/users/?search=' + condition,
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#user-info-table').html("");
            users = resp.results;
            $.each(users, function (index, user) {

                $('#user-info-table').append(
                    '<tr>' +
                        "<td>"+user.username+"</td>" +
                        "<td>"+user.phone+"</td>" +
                        "<td>"+user.role+"</td>" +
                        "<td>" +
                            "<button class='btn btn-primary'>设置</button>" +
                            "<button class='btn btn-danger' style='margin-left: 20px'>删除</button>" +
                        "</td>" +
                    "</tr>"
                )

            })

        },
        error: function () {

        }

    });
}
function create_users_select() {
    $.each(users, function (index, user) {
        var option = "<option value='"+user.id+"'>"+user.username+"</option>";
        $('#user-select').append(option);
    })

}
// storagesites
function create_storagesites_select(storagesite_name) {
    var options = "";
    $.each(storagesites, function (index, storagesite) {
        if(storagesite_name == storagesite.id){
            options += "<option value='"+storagesite.id+"' selected='selected'>"+storagesite.name+"</option>";
        }else {
            options += "<option value='"+storagesite.id+"'>"+storagesite.name+"</option>";
        }
    })
    var select = "<select type='button' class='btn btn-default'>" +
                     options +
                 "</select>"
    return select;
}
function create_lab_select(storagesite_name) {
    var options = "";
    $.each(laboratories, function (index, storagesite) {
        if(storagesite_name == storagesite.id){
            options += "<option value='"+storagesite.id+"' selected='selected'>"+storagesite.name+"</option>";
        }else {
            options += "<option value='"+storagesite.id+"'>"+storagesite.name+"</option>";
        }
    })
    var select = "<select type='button' class='btn btn-default' name='lab'>" +
                     options +
                 "</select>"
    return select;
}
function get_storagesites(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        async: false,
        url: '/api/v1/admin/storagesites/?search=' + condition,
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#storagesites-info-table').html("");
            storagesites = resp.results;
            $.each(storagesites, function (index, storagesite) {
                var tr = "<tr>" +
                         "<td class='col-sm-3'><input name='name' class='form-control' type='text' value="+storagesite.name+" /></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+storagesite.remark+"></td>"+
                         "<td>" +
                            "<button class='btn btn-primary save-storagesite' onclick='save_storagesite(this, "+JSON.stringify(storagesite)+")'>保存</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_storagesite(this,"+JSON.stringify(storagesite)+")'>删除</button>" +
                         "</td>" +
                         "</tr>";
                $('#storagesites-info-table').append(tr);
            })
        },
        error: function () {

        }

    });
}
function save_storagesite(obj, storagesite) {
    var name = $(obj).parent().prev().prev().children().val();
    var remark = $(obj).parent().prev().children().val();
    storagesite.name = name;
    storagesite.remark = remark;
    $.ajax({
        url: '/api/v1/admin/storagesites/' + storagesite.id + '/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: storagesite,
        dataType: 'json',
        type: 'PATCH',
        success: function (resp) {
            show_change_success();
        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}
function remove_storagesite(obj, storagesite) {
    var tr = $(obj).parent().parent();
    $.ajax({
        url: '/api/v1/admin/storagesites/' + storagesite.id + '/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: storagesite,
        dataType: 'json',
        type: 'DELETE',
        success: function (resp) {
            alert('删除成功');
            tr.remove();
        },
        error: function () {

        }

    });
}
function add_storagesite() {
    $.ajax({
        url: '/api/v1/admin/storagesites/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#add-storagesites-form').serialize(),
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            //$('#storagesites-info-table').html("");
            console.log(resp);
            $('#addStorageSitesModal').modal('hide');
            var tr = "<tr>" +
                         "<td><input name='name' class='form-control left' type='text' value="+resp.name+" /></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+resp.remark+"></td>"+
                         "<td>" +
                            "<button class='btn btn-primary save-storagesite' onclick='save_storagesite(this,"+JSON.stringify(resp)+")'>保存</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_storagesite(this,"+JSON.stringify(resp)+")'>删除</button>" +
                         "</td>" +
                     "</tr>";
            $('#storagesites-info-table').append(tr);
        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}

// laboratory
function get_laboratories(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        async: false,
        url: '/api/v1/admin/laboratories/?search=' + condition,
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            laboratories = resp.results;
            $('#laboratories-info-table').html("");
            $.each(laboratories, function (index, storagesite) {
                var tr = "<tr>" +
                         "<td class='col-sm-3'><input name='name' class='form-control' type='text' value="+storagesite.name+" /></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+storagesite.remark+"></td>"+
                         "<td>" +
                            "<button class='btn btn-primary' onclick='save_laboratories(this, "+JSON.stringify(storagesite)+")'>保存</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_laboratories(this,"+JSON.stringify(storagesite)+")'>删除</button>" +
                         "</td>" +
                         "</tr>";
                $('#laboratories-info-table').append(tr);
            })
        },
        error: function () {

        }

    });
}
function save_laboratories(obj, storagesite) {
    var name = $(obj).parent().prev().prev().children().val();
    var remark = $(obj).parent().prev().children().val();
    storagesite.name = name;
    storagesite.remark = remark;
    $.ajax({
        url: '/api/v1/admin/laboratories/' + storagesite.id + '/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: storagesite,
        dataType: 'json',
        type: 'PATCH',
        success: function (resp) {
            show_change_success();
        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}
function remove_laboratories(obj, storagesite) {
    var tr = $(obj).parent().parent();
    $.ajax({
        url: '/api/v1/admin/laboratories/' + storagesite.id + '/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: storagesite,
        dataType: 'json',
        type: 'DELETE',
        success: function (resp) {
            alert('删除成功');
            tr.remove();
        },
        error: function () {

           }

    });
}
function add_laboratories() {
    $.ajax({
        url: '/api/v1/admin/laboratories/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#add-laboratories-form').serialize(),
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            //$('#storagesites-info-table').html("");
            console.log(resp);
            $('#addLaboratoriesModal').modal('hide');
            var tr = "<tr>" +
                         "<td><input name='name' class='form-control left' type='text' value="+resp.name+" /></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+resp.remark+"></td>"+
                         "<td>" +
                            "<button class='btn btn-primary save-storagesite' onclick='save_laboratories(this,"+JSON.stringify(resp)+")'>保存</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_laboratories(obj=this,"+JSON.stringify(resp)+")'>删除</button>" +
                         "</td>" +
                     "</tr>";
            $('#laboratories-info-table').append(tr);
        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}

//approve

function add_approves() {
    $.ajax({
        url: '/api/v1/admin/approves/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#add-approves-form').serialize(),
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            //$('#storagesites-info-table').html("");
            console.log(resp);
            $('#addApproveModal').modal('hide');
            var tr = "<tr>" +
                         "<td>"+resp.user_vo.username+"</td>"+
                         "<td>"+approve_type[resp.type]+"</td>"+
                         "<td>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_laboratories(obj=this,"+JSON.stringify(resp)+")'>删除</button>" +
                         "</td>" +
                     "</tr>";
            $('#approves-info-table').append(tr);
        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}
function get_approves() {
    $.ajax({
        url: '/api/v1/admin/approves/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#add-approves-form').serialize(),
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            //$('#storagesites-info-table').html("");
            approves = resp.results;
            $.each(approves, function (index, approve) {
                var tr = "<tr>" +
                         "<td>"+approve.user_vo.username+"</td>"+
                         "<td>"+approve_type[approve.type]+"</td>"+
                         "<td>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_laboratories(obj=this,"+JSON.stringify(resp)+")'>删除</button>" +
                         "</td>" +
                     "</tr>";
                $('#approves-info-table').append(tr);
            })
            $('#addApproveModal').modal('hide');

        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}
var approve_type = {
    "0": "采购",
    "1": "领用"
}