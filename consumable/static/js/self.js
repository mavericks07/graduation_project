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
                    "</tr>"
                )
            })
            $('#mypicklistModal').modal('toggle');

        },
        error: function () {
            toastr.warning('', '您还没领用耗材')

        }

    });
}