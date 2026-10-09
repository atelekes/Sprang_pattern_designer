extends Control

var file_access_web
func _ready() -> void:
	get_window().files_dropped.connect(_on_file_dialog_files_dropped)
	if OS.has_feature("web"):
		file_access_web = FileAccessWeb.new()
		file_access_web.loaded.connect(on_web_file_loaded)

func _on_create_button_down() -> void:
	get_tree().call_deferred("change_scene_to_file", ("res://scenes/editor.tscn"))


func _on_load_button_down() -> void:
	$Label.show()
	if OS.has_feature("web"):
		file_access_web.open("*.png, *.json")
	else:
		$FileDialog.popup_centered()


func _on_file_dialog_file_selected(path: String) -> void:
	Global.load_path = path
	get_tree().call_deferred("change_scene_to_file", ("res://scenes/editor.tscn"))


func _on_file_dialog_files_dropped(files: PackedStringArray) -> void:
	$FileDialog.hide()
	_on_file_dialog_file_selected(files[0])

func on_web_file_loaded(file_name: String, _file_type: String, base64_data: String) -> void:
	var buffer: PackedByteArray = Marshalls.base64_to_raw(base64_data)
	
	var save_path: String = "user://" + file_name
	
	var file := FileAccess.open(save_path, FileAccess.WRITE)
	if file:
		file.store_buffer(buffer)
		file.close()
		
		$Label.hide()
		Global.load_path = save_path
		get_tree().call_deferred("change_scene_to_file", "res://scenes/editor.tscn")
