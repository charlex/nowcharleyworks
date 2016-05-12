$(document).ready(function(){

    $(".timeago").timeago();
    $("#past-things li:first").addClass("first");
    $("#input-form").submit(function(e){
        e.preventDefault()
        process_save();
    });

    $("#past-things").on("click", ".thing .archive-thing", function(e){
        e.preventDefault()
        var pk = $(this).parents(".thing").attr("data-pk");
        process_archive(pk);
    });

    $("#past-things").on("click", ".thing .delete-thing", function(e){
        e.preventDefault()
        var pk = $(this).parents(".thing").attr("data-pk");
        process_delete(pk);
    });

    $("#past-things").on("click", ".thing .thing-name", function(e){
        e.preventDefault()
        var text = $(this).text();
        $input_form = $("input", {
            val: text
        });
        console.log($input_form);
        $(this).innerHtml($input_form);
    });

    var process_save = function(){
        var name = $("#thing-input").val();
        $.ajax({
            url: "/thing/save/",
            type: "POST",
            data: {
                "name": name,
                "csrfmiddlewaretoken": Window.CSRF_TOKEN
            },
            success: function(data){
                $("#past-things li").removeClass("first");
                $("#thing-input").val("");
                $("#past-things").prepend(
                    "<li class='thing hidden' data-pk='" + data["pk"] + "'>"+
                    "<span class='thing-name'>" + name + "</span> "+
                    "<time class='thing-create-datetime timeago' datetime='" + data["created_iso8601"] + "'>" + data["created_iso8601"] + "</time> "+
                    "<a hre='#' class='archive-thing'>Archive</a></li>"
                );
                $(".timeago").timeago();
                $(".thing.hidden").slideDown(function(){
                    $(this).removeClass("hidden");
                    $("#past-things li:first").addClass("first");
                });
            }
        })
    };

    var process_archive = function(pk){
        $.ajax({
            url: "/thing/archive/",
            type: "POST",
            data: {
                "pk": pk,
                "csrfmiddlewaretoken": Window.CSRF_TOKEN
            },
            success: function(data){
                $e = $(".thing[data-pk='"+ pk +"']");
                $e.slideUp("slow", function(){
                    $e.remove();
                    $("#past-things li:first").addClass("first");

                });
            }
        });
    };

    var process_delete = function(pk){
        $.ajax({
            url: "/thing/delete/",
            type: "POST",
            data: {
                "pk": pk,
                "csrfmiddlewaretoken": Window.CSRF_TOKEN
            },
            success: function(data){
                $e = $(".thing[data-pk='"+ pk +"']");
                $e.slideUp("slow", function(){
                    $e.remove();
                    $("#past-things li").removeClass("first");
                    $("#past-things li:first").addClass("first");
                });
            }
        });
    };
});
