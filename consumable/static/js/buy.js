/**
 * Created by eason on 16-11-27.
 */


$(function () {

    $('#add-suppliers-btn').click(function () {
       $('#addSupplierModal').modal('toggle');
        console.log(laboratories);
    });
    $('#add-supplier-btn').click(function () {
        add_supplier();
    });
});

function add_supplier() {
    $.ajax({
        url: '/api/v1/admin/suppliers/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#add-supplier-form').serialize(),
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            console.log(resp);
            $('#addSupplierModal').modal('hide');
            var tr = "<tr>" +
                         "<td><input name='name' class='form-control left' type='text' value="+resp.name+" /></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+resp.phone+"></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+resp.contacts+"></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+resp.email+"></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+resp.location+"></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+resp.remark+"></td>"+
                         "<td>" +
                            "<button class='btn btn-primary save-storagesite' onclick='save_storagesite(this,"+JSON.stringify(resp)+")'>保存</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_supplier(this,"+JSON.stringify(resp)+")'>删除</button>" +
                         "</td>" +
                     "</tr>";
            $('#supplier-info-table').append(tr);
        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}

function get_suppliers(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        url: '/api/v1/admin/suppliers/?search=' + condition,
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#supplier-info-table').html("");
            var suppliers = resp.results;
            $.each(suppliers, function (index, supplier) {
                $('#supplier-info-table').append(
                    "<tr>"+
                         "<td><input name='name' class='form-control left' type='text' value="+supplier.name+" /></td>"+
                         "<td><input name='phone' class='form-control left' type='text' value="+supplier.phone+"></td>"+
                         "<td><input name='contacts' class='form-control left' type='text' value="+supplier.contacts+"></td>"+
                         "<td><input name='email' class='form-control left' type='text' value="+supplier.email+"></td>"+
                         "<td><input name='location' class='form-control left' type='text' value="+supplier.location+"></td>"+
                         "<td><input name='remark' class='form-control left' type='text' value="+supplier.remark+"></td>"+
                         "<td style='min-width: 150px'>" +
                            "<button class='btn btn-primary' onclick='save_storagesite(this,"+JSON.stringify(resp)+")'>保存</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_supplier(this,"+JSON.stringify(supplier)+")'>删除</button>" +
                         "</td>" +
                     "</tr>"
                )
            })

        },
        error: function () {

        }

    });
}
function save_supplier(obj, supplier) {
    var name = $(obj).parent().prev().prev().children().val();
    var remark = $(obj).parent().prev().children().val();
    supplier.name = name;
    supplier.remark = remark;
    $.ajax({
        url: '/api/v1/admin/suppliers/' + supplier.id + '/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: supplier,
        dataType: 'json',
        type: 'PATCH',
        success: function (resp) {
            alert('修改成功');
        },
        error: function () {

           }

    });
}
function remove_supplier(obj, supplier) {
    var tr = $(obj).parent().parent();
    $.ajax({
        url: '/api/v1/admin/suppliers/' + supplier.id + '/',
        headers:{
            Authorization: $.cookie("token")
        },
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