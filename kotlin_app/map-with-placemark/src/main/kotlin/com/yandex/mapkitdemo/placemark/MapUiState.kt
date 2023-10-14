package com.yandex.mapkitdemo.placemark

import com.yandex.mapkit.GeoObject
import com.yandex.mapkit.geometry.Point


data class ResponseItem(
    val point: Point
)

data class AtmItem(
    val address: String,
    val latitude: Double,
    val longitude: Double,
    val allDay: Boolean
)