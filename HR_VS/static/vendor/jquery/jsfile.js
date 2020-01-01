//t jquery from 'vendor/jquery/jquery.min.js'


var tbl
var del_Res
var $row
function displaydata (val){
  $(val).dataTable()
 

}

function del1(val, objTable){
    //alert(val)
//tbl= $(ID).DataTable()
// var $row=''
   $('#dataTables-example').on("click", ".fa-trash", function(){
      $row=$(this).closest('tr');
   // tbl.row($(this).parents('tr')).remove().draw(false)
     })
//   $('.fa-trash').on("click", function(){
//     var $row=$(this).closest('tr');
//   })
//res=   
// id=val
  // alert(val)
    $.ajax({
        method:'POST',
        //dataType: 'json',
        //
        url:'/storeapp/delete/',
        //contentType: 'application/json',
        
        data:{"id":val,"objTable":objTable},
        success:function(response){
           
           $row.empty()
         
        
        }
    })
}



//pass data as val id is mapped to id of the input name
function modalfill(val=[],Id=[]){
    alert("called")
    var i=0
    while (val[i]){
        $(Id[i]).val(val[i])
        i++
    }
   // alert("we have it "+$(Id[0]).val(val[1]))
    
}

