frappe.ui.form.on("Cosmetic Formula", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.status === "Approved" && !frm.doc.bom) {
			frm.add_custom_button(__("Tạo BOM"), () => {
				frm.call("make_bom").then((r) => {
					if (r.message) {
						frappe.set_route("Form", "BOM", r.message);
					}
				});
			});
		}
	},
});
