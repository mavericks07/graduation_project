/**
 * Created by eason on 16-11-29.
 */
var classifications, stocks, picklist;
$(function () {
    $('#add-classifications-btn').click(function () {
       $('#addClassificationModal').modal('toggle');
    });
    $('#add-classification-btn').click(function () {
        add_classification();
    });
    $('#add-stocks-btn').click(function () {
       $('#addStockModal').modal('toggle');
    });
    $('#add-stock-btn').click(function () {
        add_stock();
    });
    $('#pick-stock-btn').click(function () {
        stock_id = $('#pick-stock-form input[name="stock"]').val();
        add_pick(stock_id);
    });
    $('#pick-list-btn').click(function () {
        get_picklist();
    });
    $('#remove-pick-list-btn').click(function () {
        remove_picklist();
    });
    $('#update-stock-btn').click(function () {
        stock_id = $('#update-stock-form input[name="id"]').val();
        update_stock(stock_id);
    });
    $('#classification').append(create_classification_select());
    $('#storagesite').append(create_storagesites_select());
    get_classifications();
    get_stocks();
    $('#lab').append(create_lab_select());
    // var a = create_classification_select();
    // console.log(a);

});
// classifications
function add_classification() {
    $.ajax({
        url: '/api/v1/admin/classifications/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#add-classification-form').serialize(),
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            console.log(resp);
            $('#addClassificationModal').modal('hide');
            var tr = "<tr>" +
                         "<td><input name='name' class='form-control left' type='text' value="+resp.name+" /></td>"+
                         "<td>" +
                            "<button class='btn btn-primary save-storagesite' onclick='save_classification(this,"+JSON.stringify(resp)+")'>保存</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_supplier(this,"+JSON.stringify(resp)+")'>删除</button>" +
                         "</td>" +
                     "</tr>";
            $('#classification-info-table').append(tr);
        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}

function get_classifications(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        async: false,
        url: '/api/v1/admin/classifications/?search=' + condition,
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#classification-info-table').html("");
            classifications = resp.results;
            $.each(classifications, function (index, classification) {
                $('#classification-info-table').append(
                    "<tr>"+
                         "<td><input name='name' class='form-control left' type='text' value="+classification.name+" /></td>"+
                         "<td style='min-width: 150px'>" +
                            "<button class='btn btn-primary' onclick='save_classification(this,"+JSON.stringify(classification)+")'>保存</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_classification(this,"+JSON.stringify(classification)+")'>删除</button>" +
                         "</td>" +
                     "</tr>"
                )
            })

        },
        error: function () {

        }

    });
}
function save_classification(obj, classification) {
    var name = $(obj).parent().prev().children().val();
    classification.name = name;
    $.ajax({
        url: '/api/v1/admin/classifications/' + classification.id + '/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: classification,
        dataType: 'json',
        type: 'PATCH',
        success: function (resp) {
            alert('修改成功');
        },
        error: function () {

           }

    });
}
function remove_classification(obj, classification) {
    var tr = $(obj).parent().parent();
    $.ajax({
        url: '/api/v1/admin/classifications/' + classification.id + '/',
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

//stocks
function create_classification_select(classification_name) {
    var options = "";
    $.each(classifications, function (index, classification) {
        if(classification_name == classification.id){
            options += "<option value='"+classification.id+"' selected='selected'>"+classification.name+"</option>";
        }else {
            options += "<option value='"+classification.id+"'>"+classification.name+"</option>";
        }
    })
    var select = "<select type='button' class='btn btn-default'>" +
                     options +
                 "</select>"
    return select;
}
function create_add_stock_data() {
    return {
        "consumable":{
		    "name": $('#add-stock-form input[name="consumable_name"]').val(),
		    "article_number": $('#add-stock-form input[name="article_number"]').val(),
		    "unit": $('#add-stock-form input[name="unit"]').val(),
		    "brand": $('#add-stock-form input[name="brand"]').val(),
		    "classification": $('#classification select').val()
	    },
	    "number": $('#add-stock-form input[name="number"]').val(),
	    "storagesite": $('#storagesite select').val()
    }

}
function add_stock() {
    console.log(JSON.stringify(create_add_stock_data()));
    $.ajax({
        url: '/api/v1/admin/stocks/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: JSON.stringify(create_add_stock_data()),
        dataType: 'json',
        type: 'POST',
        contentType: "application/json; charset=utf-8",

        success: function (resp) {
            show_change_success();
            console.log(resp);
            $('#addStockModal').modal('hide');
                var stock = resp;
                stocks.push(stock);
                console.log(stocks);
                var consumable = stock.consumable_vo;
                $('#stock-info-table').append(
                    "<tr>"+
                         "<td>"+consumable.name+"</td>"+
                        "<td>"+consumable.brand+"</td>"+
                        "<td>"+consumable.article_number+"</td>"+
                        "<td>"+consumable.unit+"</td>"+
                        "<td>"+stock.number+"</td>"+
                        "<td>" + create_classification_select(consumable.classification_vo.id) +"</td>"+
                         "<td>" + create_storagesites_select(stock.storagesite_vo.id) +"</td>"+
                         "<td style='min-width: 250px'>" +
                            "<button class='btn btn-primary' onclick='show_update_modal(this,"+JSON.stringify(stock)+")'>入库</button>" +
                            "<button class='btn btn-primary remove-btn' onclick='pick_consumable("+JSON.stringify(stock)+")'>领用</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_classification(this,"+JSON.stringify(stock)+")'>删除</button>" +
                         "</td>" +
                     "</tr>"
                )

        },
        error: function () {
            toastr.error('', '请输入完整信息');
        }

    });
}
function pick_consumable(stock) {
    var stock_input = "<input value='"+stock.id+"' name='stock' type='hidden'/>";
    $('#pick-stock-form').append(stock_input);
    $('#pickStockModal').modal('toggle');
}

function get_stocks(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        url: '/api/v1/admin/stocks/?search=' + condition,
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#stock-info-table').html("");
            stocks = resp.results;
            $.each(stocks, function (index, stock) {
                var consumable = stock.consumable_vo

                $('#stock-info-table').append(
                    "<tr id='"+stock.id+"'>"+
                         "<td>"+consumable.name+"</td>"+
                        "<td>"+consumable.brand+"</td>"+
                        "<td>"+consumable.article_number+"</td>"+
                        "<td>"+consumable.unit+"</td>"+
                        "<td>"+stock.number+"</td>"+
                        "<td>" + create_classification_select(consumable.classification_vo.id) +"</td>"+
                         "<td>" + create_storagesites_select(stock.storagesite_vo.id) +"</td>"+
                         "<td style='min-width: 250px'>" +
                            "<button class='btn btn-primary' onclick='show_update_modal(this,"+JSON.stringify(stock)+")'>入库</button>" +
                            "<button class='btn btn-primary remove-btn' onclick='pick_consumable("+JSON.stringify(stock)+")'>领用</button>" +
                            "<button class='btn btn-danger remove-btn' onclick='remove_classification(this,"+JSON.stringify(stock)+")'>删除</button>" +
                         "</td>" +
                     "</tr>"
                )
            })

        },
        error: function () {

        }

    });
}
function show_update_modal(obj, stock) {
    $('#update-stock-form input[name="id"]').val(stock.id);
    $('#updateStockModal').modal('toggle');
}
function update_stock(stock) {

    $.ajax({
        url: '/api/v1/admin/stocks/' + stock + '/stock/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#update-stock-form').serialize(),
        dataType: 'json',
        type: 'PATCH',
        success: function (resp) {
            $('#updateStockModal').modal('hide');
            get_stocks();
            show_change_success();
        },
        error: function () {

           }

    });
}
function remove_stock(obj, stock) {
    var tr = $(obj).parent().parent();
    $.ajax({
        url: '/api/v1/admin/stocks/' + stock.id + '/',
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
// pick
function add_pick(stock_id) {
    console.log(stocks);
    $.ajax({
        url: '/api/v1/admin/stocks/' + stock_id + '/pick/',
        headers:{
            Authorization: $.cookie("token")
        },
        data: $('#pick-stock-form').serialize(),
        dataType: 'json',
        type: 'POST',

        success: function (resp) {
            toastr.success('', '已加入领用单');
            $('#pickStockModal').modal('hide');
            get_stocks();
            // get_picklist();
        },
        error: function (resp) {
            var msg = get_error_msg(resp)
            toastr.error('', msg);
        }
    });
}

function get_picklist(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        url: '/api/v1/admin/stocks/picklist/',
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'GET',
        success: function (resp) {
            $('#pick-list-info-table').html("");
            picklist = resp;
            $.each(picklist, function (index, pick) {
                var stock = pick.stock_vo
                var lab = pick.lab_vo
                var consumable = stock.consumable_vo
                $('#pick-list-info-table').append(
                    "<tr>" +
                    "<td>"+consumable.name+"</td>" +
                    "<td>"+consumable.unit+"</td>" +
                    "<td>"+pick.number+"</td>" +
                    "<td>"+lab.name+"</td>" +
                    "</tr>"
                )
            })
            $('#picklistModal').modal('toggle');

        },
        error: function () {
            toastr.warning('', '您还没领用耗材')

        }

    });
}
function remove_picklist(condition) {
    if(condition==undefined){
        condition = '';
    }
    $.ajax({
        url: '/api/v1/admin/stocks/picklist/',
        headers:{
            Authorization: $.cookie("token")
        },
        dataType: 'json',
        type: 'DELETE',
        success: function (resp) {
            $('#picklistModal').modal('hide');
            get_stocks();
        },
        error: function () {

        }

    });
}