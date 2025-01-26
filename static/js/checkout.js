

function adCheck(user, totalDays) {
    const baseURL = window.location.origin;
    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    const showLoader = () => $("#py-up").show();
    const hideLoader = () => $("#py-up").hide();

    const updateDiscounts = (response) => {
        const {
            username,
            room_cost: roomCostPerDay,
            res_cost: restaurantCost,
            advance_amt: advanceAmount,
            remaing_balance: remainingBalance,
            room_discount: prevRoomDiscount,
            resturet_discount: prevRestaurantDiscount,
        } = response;

        const roomAmount = roomCostPerDay * totalDays;

        $("#prev_restu_disc").html(
            `<p class="text-dark">Previous Restaurant Discount: <i class="text-warning h5">${prevRestaurantDiscount}</i></p>`
        );
        $("#prev_room_disc").html(
            `<p class="text-dark">Previous Room Discount: <i class="text-danger h5">${prevRoomDiscount}</i></p>`
        );

        $("#idss_full_name").val(username);
        $("#rem_blc").val(remainingBalance);
        $("#idss_organization").val(roomAmount);
        $("#id_Resturent_amt").val(restaurantCost);
        $("#advance_amt").val(advanceAmount);
        $("#res_desc").val(0);
        $("#id_room_discount").val(0);

        calculateAmounts(roomCostPerDay, totalDays); // Ensure calculations are updated instantly
    };

    const calculateAmounts = (roomCostPerDay = 0, totalDays = 0) => {
        const roomDiscount = parseFloat($("#id_room_discount").val()) || 0;
        const roomAmount = (roomCostPerDay && totalDays) ? roomCostPerDay * totalDays : parseFloat($("#idss_organization").val()) || 0;
        const resDiscount = parseFloat($("#res_desc").val()) || 0;
        const restaurantCost = parseFloat($("#id_Resturent_amt").val()) || 0;
        const advanceAmount = parseFloat($("#advance_amt").val()) || 0;
        const remainingBalance = parseFloat($("#rem_blc").val()) || 0;
        const vatApplied = $("#check1").prop("checked");

        const roomAfterDiscount = roomAmount - roomDiscount;
        const restaurantAfterDiscount = restaurantCost - resDiscount;
        const afterDiscountTotal = roomAfterDiscount + restaurantAfterDiscount;

        const vat = vatApplied ? (afterDiscountTotal * 13) / 100 : 0;
        $("#vat_count").val(vat);

        const payableAmount = roomAfterDiscount + restaurantAfterDiscount + vat + remainingBalance - advanceAmount;
        const amountPaid = payableAmount - parseFloat($("#last_value").val() || 0);

        $("#ids_total_amt").val(payableAmount);
        $("#amount_paid").val(amountPaid);

        $("#calc-details").html(`
            <div class="row" id="get_data">
                <div class="col-md-6 py-1">
                    <label for="advance_amt" class="py-1 h6">Room Discount:</label>
                </div>
                <div class="col-md-6 py-1">
                    <input type="text" class="form-control" value="${roomAfterDiscount}" id="room-discount" readonly>
                </div>
                <div class="col-md-6 py-1">
                    <label for="resturent_discount" class="py-1 h6">Restaurant Discount:</label>
                </div>
                <div class="col-md-6 py-1">
                    <input type="text" class="form-control" value="${restaurantAfterDiscount}" id="resturent_discount" readonly>
                </div>
            </div>
        `);
    };

    const processCheckout = () => {
        const data = {
            user,
            resturent_discount: $("#res_desc").val(),
            room_discount: $("#id_room_discount").val(),
            vat: $("#vat_count").val(),
            remarks: $("#remarks").val(),
            remaing_amt: $("#amount_paid").val(),
        };

        $.ajax({
            method: 'POST',
            url: `${baseURL}/check_out_process/`,
            dataType: 'json',
            headers: { "X-CSRFToken": csrfToken },
            data,
            success: (resp) => {
                if (resp.msg === "User Check Out successfully") {
                    window.location.replace(baseURL);
                } else {
                    $("#brek_point").modal('toggle');
                    $.notify("User cannot check out!", "error");
                }
            },
            error: () => {
                $.notify("Please fill all the required fields", "error");
            },
        });
    };

    // AJAX request to fetch initial data
    $.ajax({
        method: 'POST',
        url: `${baseURL}/check_out/`,
        dataType: 'json',
        headers: { "X-CSRFToken": csrfToken },
        data: { user },
        beforeSend: showLoader,
        success: updateDiscounts,
        complete: hideLoader,
    });

    // Event Listeners for real-time updates
    $("#id_room_discount, #res_desc, #id_Resturent_amt, #idss_organization, #advance_amt, #rem_blc").on("input", () => calculateAmounts());
    $("#check1").on("change", () => calculateAmounts());
    $("#rms_chk").on("click", processCheckout);

function ad_check(a) {
    var base_url = window.location.origin;
    var user = a;
    var csr = $("input[name=csrfmiddlewaretoken]").val();
    cred = { "user": user }
    $.ajax({
        method: 'POST',
        url: base_url + "/check_out/",
        dataType: "json",
        headers: { "X-CSRFToken": csr },
        data: cred,
        beforeSend: function () {
            $("#py-up").show()
        },
        success: function (response) {
            var full_name = response.username
            var room_amount = response.room_cost
            var res_cost = response.res_cost
            var advance_amt = response.advance_amt
            var rem_blnce = response.remaing_balance
            var prev_room_disc = response.room_discount
            var prv_restu_disc = response.resturet_discount

            $("#prev_restu_disc").html(`<p class="text-dark">Previous Restaurant Discount Is: <i class="text-warning h5">${prv_restu_disc}</i></p>`)
            $("#prev_room_disc").html(`<p class="text-dark">Previous Room Discount Is: <i class="text-danger h5"> ${prev_room_disc}</i></p>`)
            $("#idss_full_name").val(full_name)
            $("#rem_blc").val(rem_blnce)
            $("#idss_organization").val(room_amount)
            $("#id_Resturent_amt").val(res_cost)
            $("#advance_amt").val(advance_amt)
            $("#res_desc").val(0)
            $("#id_room_discount").val(0)
        },
        complete: function () {
            $("#py-up").hide()
        }
    });

    $(".ky-up").keypress(function () {
        var output = '';

        var rm_dis = parseFloat($("#id_room_discount").val()) || 0;
        var checkbox_r = $("#check1").prop("checked");
        var room_amount = parseFloat($("#idss_organization").val()) || 0;
        var res_cost = parseFloat($("#id_Resturent_amt").val()) || 0;
        var res_disc = parseFloat($("#res_desc").val()) || 0;
        var advance_amt = parseFloat($("#advance_amt").val()) || 0;
        var vat = parseFloat($("#vat_count").val()) || 0;
        var room_discount = parseFloat($("#room-discount").val()) || 0;
        var resturent_discount = parseFloat($("#resturent_discount").val()) || 0;
        var rem_blc = parseFloat($("#rem_blc").val()) || 0;

        // Room discount and restaurant discount
        if (rm_dis !== "" && res_cost !== "") {
            var room_disc = room_amount - rm_dis;
            var res_desc = res_cost - res_disc;
            var after_disc = room_disc + res_desc;
        }

        // Calculate VAT based on the checkbox
        if (checkbox_r === true) {
            vat = after_disc * 13 / 100;
            $("#vat_count").val(vat);
        } else {
            vat = 0; // Ensure VAT is set to 0 when unchecked
            $("#vat_count").val(0);
        }

        // Calculate payable amount
        var payable_amt = room_discount + vat + resturent_discount + rem_blc - advance_amt;
        $("#ids_total_amt").val(payable_amt);

        // Amount paid calculation
        var amount_paid = payable_amt - parseFloat($("#last_value").val());
        $("#amount_paid").val(amount_paid);

        var inner_data = `
        <div class="row" id ="get_data">
            <div class="col-md-6 py-1">
                <label for="advance_amt" class="py-1 h6">Room Discount:</label>
            </div>
            <div class="col-md-6 py-1">
                <input type="text" class="form-control" value="${room_disc}" id="room-discount" name="room-discount" placeholder="" readonly="">
            </div>
            <div class="col-md-6 py-1">
                <label for="resturent_discount" class="py-1 h6">Restaurant Discount:</label>
            </div>
            <div class="col-md-6 py-1">
                <input type="text" class="form-control" value="${res_desc}" id="resturent_discount" name="resturent_discount" placeholder="" readonly="">
            </div>
        </div>
        `;

        output += $("#calc-details").html(inner_data);
    });

    $("#rms_chk").unbind("click").bind("click", function () {
        var user = a;
        var resturent_discount = $("#res_desc").val();
        var room_discount = $("#id_room_discount").val();
        var vat = $("#vat_count").val();
        var remarks = $("#remarks").val();
        var remaing_amt = $("#amount_paid").val();

        var csr = $("input[name=csrfmiddlewaretoken]").val();
        data = {
            "user": a, "resturent_discount": resturent_discount,
            "room_discount": room_discount, "vat": vat, "remarks": remarks, "remaing_amt": remaing_amt
        };
        $.ajax({
            method: 'POST',
            url: base_url + "/check_out_process/",
            dataType: "json",
            headers: { "X-CSRFToken": csr },
            data: data,
            success: function (resp) {
                if (resp.msg === "User Check Out successfully") {
                    window.location.replace(base_url);
                } else {
                    $("#brek_point").modal('toggle');
                    $.notify("User Can't checkout !!!", "error");
                }
            },
            error: function () {
                $.notify("User can't checkout. Please fill the empty fields.", "error");
            }
        });
    });

}
