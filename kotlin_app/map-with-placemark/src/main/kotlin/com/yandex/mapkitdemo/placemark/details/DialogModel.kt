package com.yandex.mapkitdemo.placemark.details

import android.app.AlertDialog
import android.content.Context
import com.yandex.mapkitdemo.placemark.AtmItem
import com.yandex.mapkitdemo.placemark.OfficeItem

class DialogModel(private val context: Context) {

    // Метод для отображения диалогового окна с информацией о atmItem
    fun showInfoDialogAtm(atmItem: AtmItem) {
        val builder = AlertDialog.Builder(context)
        builder.setTitle("Информация о банкомате")
        builder.setMessage("Адрес: ${atmItem.address}\nДругая информация: будет оторбражена тут")

        builder.setPositiveButton("Закрыть") { dialog, _ ->
            dialog.dismiss()
        }

        val dialog = builder.create()
        dialog.show()
    }

    fun showInfoDialogOffice(officeItem: OfficeItem) {
        val builder = AlertDialog.Builder(context)
        builder.setTitle("Информация об Отделении")
        builder.setMessage(
            "Адрес: ${officeItem.address}\n" +
                    "КОРДЫ: ${officeItem.latitude} ${officeItem.longitude}" +
                    "Режим работы: ${officeItem.openHours}\n" +
                    "Номер телефона: +7912345789\n" +
                    "Метро: ${officeItem.metroStation}"
        )

        builder.setNeutralButton("Встать в очередь") { dialog, _ -> }

        val dialog = builder.create()
        dialog.show()
    }
}
