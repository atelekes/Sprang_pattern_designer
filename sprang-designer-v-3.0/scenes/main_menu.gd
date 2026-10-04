extends Control

func _on_create_button_down() -> void:
	get_tree().call_deferred("change_scene_to_file", ("res://scenes/editor.tscn"))


func _on_load_button_down() -> void:
	$FileDialog.popup_centered()



func _on_file_dialog_file_selected(path: String) -> void:
	Global.load_path = path
	get_tree().call_deferred("change_scene_to_file", ("res://scenes/editor.tscn"))
