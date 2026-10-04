extends Control

func _on_rows_value_changed(value: float) -> void:
	Global.rows = int(value)
	get_node("../../Grid").queue_redraw()
	Global.mark_changed.emit()
	
func _on_columns_value_changed(value: float) -> void:
	Global.columns = int(value)
	get_node("../../Grid").queue_redraw()
	Global.mark_changed.emit()
