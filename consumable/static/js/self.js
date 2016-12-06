/**
 * Created by eason on 16-12-5.
 */
var mypicklist;
$(function () {
get_my_application();
get_my_approves();
})

// my approves
function get_my_approves(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        url: '/api/v1/admin/picklist/myapprove/',
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#my-approves-info-table').html("");
            mypicklist = resp;
            $.each(mypicklist, function (index, pick) {
                var user = pick.user_vo;
                console.log(user);
                $('#my-approves-info-table').append(
                    "<tr>" +
                    "<td>"+user.username+"</td>" +
                    "<td>"+pick.status_name+"</td>" +
                    "<td style='min-width: 250px'>" +
                            "<button class='btn btn-primary' onclick='get_picklist("+JSON.stringify(pick)+")'>查看</button>" +
                            "<button class='btn btn-primary remove-btn' onclick='agree_picklist("+JSON.stringify(pick)+")'>同意</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_classification(this,"+JSON.stringify()+")'>驳回</button>" +
                         "</td>" +
                    "</tr>"
                )
            })


        },
        error: function () {
        }

    });
}


function agree_picklist(picklist) {
    $.ajax({
        url: '/api/v1/admin/picklist/' + picklist.id + '/agree/',
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            get_my_approves();
            show_change_success();
        },
        error: function () {
        }
    });
}

//my application

function get_my_application(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        url: '/api/v1/admin/picklist/myapplication/',
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#my-applications-info-table').html("");
            mypicklist = resp;
            $.each(mypicklist, function (index, pick) {
                var user = pick.user_vo;
                console.log(user);
                $('#my-applications-info-table').append(
                    "<tr>" +
                    "<td>"+user.username+"</td>" +
                    "<td>"+pick.status_name+"</td>" +
                    "<td style='min-width: 250px'>" +
                            "<button class='btn btn-primary' onclick='get_picklist("+JSON.stringify(pick)+")'>查看</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_classification(this,"+JSON.stringify()+")'>取消</button>" +
                         "</td>" +
                    "</tr>"
                )
            })
        },
        error: function () {
        }

    });
}

function return_consumable(obj, pick) {
    var number = $(obj).parent().prev().children().val();
    var data = {
        'number': number
    };
    $.ajax({
        url: '/api/v1/admin/picks/' + pick.id + '/return_/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: JSON.stringify(data),
        dataType: 'json',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        success: function (resp) {
            $('#mypicklistModal').modal('hide');
            show_retuen_success();
            get_picklist(pick);
        },
        error: function (resp) {
            var msg = get_error_msg(resp)
            toastr.error('', msg);
        }

    });
}

function get_picklist(pick) {
    $.ajax({
        url: '/api/v1/admin/picklist/' + pick.id + '/detail/',
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#my-pick-list-info-table').html("");
            mypicklist = resp;
            $.each(mypicklist, function (index, pick) {
                var stock = pick.stock_vo
                var lab = pick.lab_vo
                var consumable = stock.consumable_vo
                $('#my-pick-list-info-table').append(
                    "<tr>" +
                    "<td>"+consumable.name+"</td>" +
                    "<td>"+consumable.unit+"</td>" +
                    "<td>"+pick.number+"</td>" +
                    "<td>"+lab.name+"</td>" +
                    "<td>"+pick.can_return_number+"</td>" +
                    "<td>"+pick.return_number+"</td>" +
                    "<td><input class='form-control left' style='max-width: 60px' type='number' name='number'></td>" +
                    "<td><button class='btn btn-success remove-btn' onclick='return_consumable(this, "+JSON.stringify(pick)+")'>归还</button></td>" +
                    "</tr>"
                )
            })
            $('#mypicklistModal').modal('toggle');

        },
        error: function () {
            //toastr.warning('', '您还没领用耗材')
        }

    });
}