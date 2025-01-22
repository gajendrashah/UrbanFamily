   
    function ad_check(a) {
        var base_url =  window.location.origin;
        var user = a;
        var csr = $("input[name=csrfmiddlewaretoken]").val();
        cred = { "user": user }
        $.ajax({
            method: 'POST',
            url: base_url+"/check_out/",
            dataType: "json",
            headers: { "X-CSRFToken": csr, },
            data: cred,
            beforesend: function () {
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
            
            var rm_dis = $("#id_room_discount").val()
            var checkbox_r = $("#check1").prop("checked");
            var room_amount = $("#idss_organization").val();
            var res_cost = $("#id_Resturent_amt").val();
            var res_disc = $("#res_desc").val()
            var advance_amt = $("#advance_amt").val();
            var vat = $("#vat_count").val()
            var room_discount = $("#room-discount").val()
            var resturent_discount = $("#resturent_discount").val()
            var rem_blc = $("#rem_blc").val()
            if (rm_dis !== "" && res_cost !== "") {
                var room_disc = parseFloat(room_amount) - parseFloat(rm_dis)
                var res_desc = parseFloat(res_cost) - parseFloat(res_disc)
                var after_disc = room_disc + res_desc
                
            }
            if (checkbox_r===true){
                $("#vat_count").val(after_disc * 13 / 100)
            }else{  
                $("#vat_count").val(0)
            }
            
            
            $('input[type="checkbox"]').click(function () {
        if ($(this).prop("checked") == true) {
           
            $("#vat_count").val(after_disc * 13 / 100)
        }
        else if ($(this).prop("checked") == false) {
            $("#vat_count").val(0)
           
       
        }
    });
    var payable_amt = ((parseFloat(room_discount) + parseFloat(vat) + parseFloat(resturent_discount) + parseFloat(rem_blc) - parseFloat(advance_amt)))
    $("#ids_total_amt").val(payable_amt)
    var amount_paid = payable_amt - parseFloat($("#last_value").val())
    $("#amount_paid").val(amount_paid)
    
    var inner_data = `  
<div class="row" id ="get_data" >
<div class="col-md-6 py-1">
<label for="advance_amt" class="py-1 h6">Room Discount:</label>
</div>
<div class="col-md-6 py-1">
<input type="text" class="form-control"  value = "${room_disc}" id="room-discount" name="room-discount"
placeholder="" readonly="">

</div>

<div class="col-md-6 py-1">
<label for="resturent_discount" class="py-1 h6">Resturenr Discount:</label>
</div>
<div class="col-md-6 py-1">
<input type="text" class="form-control" value = "${res_desc}" id="resturent_discount" name="resturent_discount"
placeholder="" readonly="">

</div>
</div>

`

output += $("#calc-details").html(inner_data)
           


        });
        
        
        $("#rms_chk").unbind("click").bind("click", function () {
            var user = a;
            var resturent_discount = $("#res_desc").val()
            var room_discount = $("#id_room_discount").val()
            var vat = $("#vat_count").val()
            var remarks = $("#remarks").val()
            var remaing_amt = $("#amount_paid").val()


            var csr = $("input[name=csrfmiddlewaretoken]").val();
            data = {
                "user": a, "resturent_discount": resturent_discount,
                "room_discount": room_discount, "vat": vat, "remarks": remarks, "remaing_amt": remaing_amt
            }
            $.ajax({
                method: 'POST',
                url: base_url + "/check_out_process/",
                dataType: "json",
                headers: { "X-CSRFToken": csr, },
                data: data,
                success: function (resp) {
                    if (resp.msg = "User Check Out sucessfully"){
                        // $("#staticBackdrop").modal('toggle');
                        // $.notify("User checkout successfully ", "success");

                        window.location.replace(base_url)
                       
                        
                    }else{
                        $("#brek_point").modal('toggle');
                        $.notify("User Cant checkout !!! ", "success");
                    }
                  
                   
                },
                error:function(){
                    $.notify("User cant checkou plase fill the empty value ", "error");
                        
                }
            })






        });

    }