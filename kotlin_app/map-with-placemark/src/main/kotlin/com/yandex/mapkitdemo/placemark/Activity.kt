package com.yandex.mapkitdemo.placemark

import MyApiService
import android.os.Bundle
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.yandex.mapkit.MapKitFactory
import com.yandex.mapkit.geometry.Point
import com.yandex.mapkit.map.CameraPosition
import com.yandex.mapkit.map.IconStyle
import com.yandex.mapkit.map.Map
import com.yandex.mapkit.map.MapObjectTapListener
import com.yandex.mapkit.mapview.MapView
import com.yandex.mapkitdemo.common.CommonDrawables
import com.yandex.mapkitdemo.common.CommonId
import com.yandex.mapkitdemo.common.showToast
import com.yandex.mapkitdemo.placemark.details.DialogModel
import com.yandex.runtime.image.ImageProvider
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.util.Objects

class Activity : AppCompatActivity() {
    private lateinit var mapView: MapView
    private lateinit var map: Map
    private lateinit var dialog: DialogModel


    private val placemarkTapListener = MapObjectTapListener { mapObject, point ->
        val atmItem = mapObject.userData as AtmItem
        val address = atmItem.address
        showToast("Адресс: ${address}")
        dialog.showInfoDialogAtm(atmItem)

        true
    }

    private val officeTapListener = MapObjectTapListener { mapObject, point ->
        val officeItem = mapObject.userData as OfficeItem
        val address = officeItem.address
        showToast("Адресс: ${address}")
        dialog.showInfoDialogOffice(officeItem)

        true
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        MapKitFactory.initialize(this)
        setContentView(R.layout.activity_layout)
        mapView = findViewById(R.id.mapview)
        dialog = DialogModel(this)

        val mapkitVersionView = findViewById<LinearLayout>(R.id.mapkit_version)
        val mapkitVersionTextView =
            mapkitVersionView.findViewById<TextView>(CommonId.mapkit_version_value)
        mapkitVersionTextView.text = MapKitFactory.getInstance().version

        val map = mapView.mapWindow.map
        map.move(POSITION)

        val imageProviderOffice = ImageProvider.fromResource(this, R.drawable.points)

//        runBlocking {
//            val apiService = MyApiService()
//            launch(Dispatchers.IO) {
//                // Запускаем сетевой запрос в фоновом потоке
//                val atmItems = apiService.getAtmData()
//                runOnUiThread {
//                    atmItems.forEach { atmItem ->
//                        val point = Point(atmItem.latitude, atmItem.longitude)
//                        val placemarkObject = map.mapObjects.addPlacemark(
//                            point,
//                            imageProvider,
//                            IconStyle().apply { scale = 1f }
//                        ).apply {
//                            addTapListener(placemarkTapListener)
//                            userData = atmItem
//                        }
//                    }
//                }
//            }
//        }

        runBlocking {
            val apiService = MyApiService()
            launch(Dispatchers.IO) {
                // Запускаем сетевой запрос в фоновом потоке
                val officeItems = apiService.getOfficeData(55.7131, 37.84473)
                runOnUiThread {
                    officeItems.forEach { officeItem ->
                        val point = Point(officeItem.latitude, officeItem.longitude)
                        val placemarkObject = map.mapObjects.addPlacemark(
                            point,
                            imageProviderOffice,
                            IconStyle().apply { scale = 0.1f }
                        ).apply {
                            addTapListener(officeTapListener)
                            userData = officeItem
                        }
                    }
                }
            }
        }

    }

    override fun onStart() {
        super.onStart()
        MapKitFactory.getInstance().onStart()
        mapView.onStart()
    }

    override fun onStop() {
        mapView.onStop()
        MapKitFactory.getInstance().onStop()
        super.onStop()
    }


    companion object {
        private val POINT = Point(55.751280, 37.629720)
        private val POSITION = CameraPosition(POINT, 17.0f, 150.0f, 30.0f)
    }
}
