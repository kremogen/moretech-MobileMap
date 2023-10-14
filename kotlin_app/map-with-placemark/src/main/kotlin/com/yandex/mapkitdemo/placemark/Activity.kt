package com.yandex.mapkitdemo.placemark

import MyApiService
import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.yandex.mapkit.MapKit
import com.yandex.mapkit.MapKitFactory
import com.yandex.mapkit.geometry.Point
import com.yandex.mapkit.layers.ObjectEvent
import com.yandex.mapkit.map.CameraPosition
import com.yandex.mapkit.map.IconStyle
import com.yandex.mapkit.map.Map
import com.yandex.mapkit.map.MapObjectTapListener
import com.yandex.mapkit.mapview.MapView
import com.yandex.mapkit.user_location.UserLocationObjectListener
import com.yandex.mapkit.user_location.UserLocationView
import com.yandex.mapkitdemo.common.CommonDrawables
import com.yandex.mapkitdemo.common.CommonId
import com.yandex.mapkitdemo.common.showToast
import com.yandex.mapkitdemo.placemark.details.DialogModel
import com.yandex.runtime.image.ImageProvider
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

class Activity : AppCompatActivity(), UserLocationObjectListener {
    private lateinit var mapView: MapView
    private lateinit var map: Map
    private lateinit var dialog: DialogModel
    private lateinit var locationTextView: TextView
    private lateinit var fusedLocationProviderClient: FusedLocationProviderClient
    private var latitude: Double = 0.0
    private var longitude: Double = 0.0


    private val atmTapListener = MapObjectTapListener { mapObject, point ->
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
        var mapKit: MapKit = MapKitFactory.getInstance()
        setContentView(R.layout.activity_layout)
        mapView = findViewById(R.id.mapview)
        dialog = DialogModel(this)
        val map = mapView.mapWindow.map
        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(this)
        fusedLocationProviderClient.lastLocation.addOnSuccessListener {
            latitude = it.latitude
            longitude = it.longitude
            locationTextView.text = "$latitude\n$longitude"
            val POSITION = CameraPosition(Point(latitude, longitude), 13f, 150f, 30f)
            map.move(POSITION)
            val imageProviderOffice = ImageProvider.fromResource(this, R.drawable.points)
            val imageProviderAtm = ImageProvider.fromResource(this, CommonDrawables.ic_dollar_pin)

            // ATMS
            runBlocking {
                val apiService = MyApiService()
                launch(Dispatchers.IO) {
                    // Запускаем сетевой запрос в фоновом потоке
                    val atmItems = apiService.getAtmData()
                    runOnUiThread {
                        atmItems.forEach { atmItem ->
                            val point = Point(atmItem.latitude, atmItem.longitude)
                            map.mapObjects.addPlacemark(
                                point,
                                imageProviderAtm,
                                IconStyle().apply { scale = 1f }
                            ).apply {
                                addTapListener(atmTapListener)
                                userData = atmItem
                            }
                        }
                    }
                }
            }

            // OFFICES
            runBlocking {
                val apiService = MyApiService()

                launch(Dispatchers.IO) {
                    // Запускаем сетевой запрос в фоновом потоке
                    val officeItems =
                        apiService.getOfficeData(latitude, longitude)
                    Log.d("app", "$latitude $longitude")
                    runOnUiThread {
                        officeItems.forEach { officeItem ->
                            val point = Point(officeItem.latitude, officeItem.longitude)
                            map.mapObjects.addPlacemark(
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
        requestLocationPermission()
        locationTextView = findViewById(R.id.locationTextView)

        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            return
        }

        var locationmap = mapKit.createUserLocationLayer(mapView.mapWindow)
        locationmap.isVisible = true

        val mapkitVersionView = findViewById<LinearLayout>(R.id.mapkit_version)
        val mapkitVersionTextView =
            mapkitVersionView.findViewById<TextView>(CommonId.mapkit_version_value)
        mapkitVersionTextView.text = MapKitFactory.getInstance().version


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

    private fun requestLocationPermission() {
        if (
            ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        )
            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                ), 0
            )
        return
    }


    override fun onObjectAdded(p0: UserLocationView) {
        TODO("Not yet implemented")
    }

    override fun onObjectRemoved(p0: UserLocationView) {
        TODO("Not yet implemented")
    }

    override fun onObjectUpdated(p0: UserLocationView, p1: ObjectEvent) {
        TODO("Not yet implemented")
    }
}
