// Advanced and modular version of the provided code with real-time updates

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
}
