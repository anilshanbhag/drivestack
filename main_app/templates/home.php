{% person : { username, email }, drives : [ ] %}
<!DOCTYPE HTML>
<html>
    <head>
    	<link href="bootstrap/css/bootstrap.css" rel="stylesheet">
        <style type="text/css">
            .folder_icon {
                background: url('/static/img/collectionsprite.png') no-repeat -4px 0; width: 16px!important; height: 13px!important; position: static!important; display: inline-block; line-height: normal; margin-bottom: -2px; margin-right: 7px; 
            }
            .file_icon {
                background: url('/static/img/document_icon.png') no-repeat; width: 16px!important; height: 13px!important; position: static!important; display: inline-block; line-height: normal; margin-bottom: -2px; margin-right: 7px; 
            }
            .favourite_icon {
                background: url('/static/img/star4.png') no-repeat; width: 16px!important; height: 16px!important; position: static!important; display: inline-block; line-height: normal; margin-bottom: -2px; margin-right: 7px; 
            }
            .favourite_icon:hover {
                background: url('/static/img/star-hover4.png');
            }
            .tabbed {
                padding-right: 5px;
            }
            .dropdown-unlink {
               padding: 3px 15px; 
            }
            .dull {color: #555;}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row">
                <div class="span4">
                 <h2>Drive Stack</h2>
                </div>
                <div class="span4 offset4">
                	<ul class="nav nav-pills">
						<li>
					    	<a href="#" class="btn disabled tabbed">Home</a>
					  	</li>
					  	<li><a href="#" class="tabbed">Getting Started</a></li>
                        <li class="dropdown" id="user-options">
                            <a class="dropdown-toggle" data-toggle="dropdown" href="#user-options">
                              {{ person.username }}
                              <b class="caret"></b>
                            </a>
                            <ul class="dropdown-menu">
                              <li><span class="dropdown-unlink"><strong>{{ person.username }}</strong></span></li>
                              <li><span class="dropdown-unlink">{{ person.email }}</span></li>
                              <li><span class="dropdown-unlink dull"></span></li>
                 			  # sprintf("%01.2f of %01.2f used", $boxFilled/1073741824.0 , $boxQuota/1073741824.0 );
                              <li class="divider"></li>
                              <li><a href="#">Settings</a></li>
                              <li><a href="#">LogOut</a></li>
                            </ul>
                        </li>
					</ul>
                </div>
         	<div class="row">
         		<!-- <div class="span3">
         			<ul class="nav nav-list">
         				<li class="nav-header">Dropbox</li>
					  	<li>
					    	<a href="#">
					      	<i class="icon-book"></i>
					      	Library
					    	</a>
						</li>
					</ul>
         		</div -->
         		<div class="span12" id="drive">
                    <a class="btn" data-toggle="modal" href="#fileUpload">Upload</a>
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>. </th>
                                <th>Title </th>
                                <th>Store </th>
                                <th>Last Modified </th>
                            </tr>
                        </thead>
                        <tbody id="drive-content">
                        </tbody>
                    </table>
         		</div>
         	</div>
        </div>
        <div class="modal hide fade" id="fileUpload">
             <form method="post" enctype="multipart/form-data"  action="upload.php">  
                 <input type="file" name="file" id="file" multiple />  
                 <button type="submit" id="btn">Upload Files!</button>  
                <div class="span5 fileupload-progress fade">
                    <!-- The global progress bar -->
                    <div class="progress progress-success progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100">
                        <div class="bar" style="width:0%;"></div>
                    </div>
                    <!-- The extended global progress information -->
                    <div class="progress-extended">&nbsp;</div>
                </div>
                 <div id="response"></div>
             </form> 
        </div>
    </body>
    <script type="text/html" id="drive_header">
    </script>
    <script type="text/javascript" src="bootstrap/js/jquery.min.js"></script>
    <script type="text/javascript" src="bootstrap/js/bootstrap.min.js"></script>
    <script type="text/javascript">
    // Drive Show
    var drive = document.querySelector('#drive-content'); 
    <?php if ($_SESSION['dropbox_enabled']) { ?>
    var dropboxData =  <?php echo json_encode(DropboxConvertor($dropboxFolder)); ?>;
    for (i in dropboxData['contents']) {
        var row = dropboxData['contents'][i];
        var pathArr = row['path'].split('/');
        var row_html = "<tr> <td> <span class='favourite_icon'></span> </td> <td>";
        row_html += row['is_dir'] ? "<a href='#'><span class='folder_icon'></span>" : "<a href='#'><span class='file_icon'></span>";
        row_html += pathArr[pathArr.length - 1] + "</a></td><td>" + row['origin'] + "</td><td>" + row['modified'] + "</td> </tr>";
        drive.innerHTML += row_html;
    }
    <?php } if ($_SESSION['box_enabled']) { ?>
    var boxData =  <?php echo json_encode(BoxConvertor($boxFolder)); ?>;
    for (i in boxData['contents']) {
        var row = boxData['contents'][i];
        var row_html = "<tr> <td> <span class='favourite_icon'></span> </td> <td>";
        row_html += row['is_dir'] ? "<a href='#'><span class='folder_icon'></span>" : "<a href='#'><span class='file_icon'></span>";
        row_html += row['name'] + "</a></td><td>" + row['origin'] + "</td><td>" + "</td> </tr>";
        drive.innerHTML += row_html;
    }
    <?php } ?>
    // File upload modal
    $('#fileUpload').modal({
        show: false
    });

    var input = document.getElementById("file"), 
            formdata = false;

    if (window.FormData) {
        formdata = new FormData();
        document.getElementById("btn").style.display = "none";
    }

    input.addEventListener("change", function (evt) {
        document.getElementById("response").innerHTML = "Uploading . . ."
        var i = 0, len = this.files.length, img, reader, file;
    
        for ( ; i < len; i++ ) {
            file = this.files[i];
    
            if ( window.FileReader ) {
                reader = new FileReader();
                reader.readAsDataURL(file);
            }
            if (formdata) {
                formdata.append("files[]", file);
            }
        }
    
        if (formdata) {
            $.ajax({
                url: "upload.php",
                type: "POST",
                data: formdata,
                processData: false,
                contentType: false,
                success: function (res) {
                    document.getElementById("response").innerHTML = res; 
                }
            });
        }
    }, false);
    </script>
</html>
