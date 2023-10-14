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

data class OfficeItem(
    val salePointName: String,
    val address: String,
    val status: String,
    val openHours: List<OpenHours>,
    val rko: String,
    val openHoursIndividual: List<OpenHours>,
    val officeType: String,
    val salePointFormat: String,
    val suoAvailability: String,
    val hasRamp: String,
    val latitude: Double,
    val longitude: Double,
    val metroStation: String,
    val distance: Int,
    val kep: Boolean,
    val myBranch: Boolean
)

data class OpenHours(
    val days: String,
    val hours: String
)