function addCart(id) {
            var csrf = $('input[name="csrfmiddlewaretoken"]').val()
            $.ajax({
                type:'POST',
                url:'/ttsx/addCart/',
                headers:{'X-CSRFToken': csrf},
                dataType:'json',
                data:{'g_id':id},
                success:function (data) {
                    if (data.code == '200') {
                        alert('添加购物车成功')
                    }
                }
            });
        }