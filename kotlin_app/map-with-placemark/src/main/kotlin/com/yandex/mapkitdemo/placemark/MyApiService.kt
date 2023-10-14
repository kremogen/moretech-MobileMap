import com.yandex.mapkitdemo.placemark.AtmItem
import com.yandex.mapkitdemo.placemark.OfficeItem
import com.yandex.mapkitdemo.placemark.OpenHours
import okhttp3.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import kotlin.coroutines.suspendCoroutine

class MyApiService {
    private val link = "http://192.168.1.4:8000"
    private val client = OkHttpClient()

    suspend fun getAtmData(): List<AtmItem> {
        val url = link + "/get_atm" // Замените на ваш URL

        val request = Request.Builder()
            .url(url)
            .build()

        return suspendCoroutine { continuation ->
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    // Обработка ошибки при сетевом запросе
                    continuation.resumeWith(Result.failure(e))
                }

                override fun onResponse(call: Call, response: Response) {
                    response.use {
                        if (!response.isSuccessful) {
                            // Обработка ошибки при получении ответа
                            val errorMessage = "Response unsuccessful: ${response.code()}"
                            continuation.resumeWith(Result.failure(IOException(errorMessage)))
                        } else {
                            val jsonData = response.body()?.string()
                            if (jsonData != null) {
                                val atmItems = parseAtmData(jsonData)
                                continuation.resumeWith(Result.success(atmItems))
                            } else {
                                val errorMessage = "Response body is empty"
                                continuation.resumeWith(Result.failure(IOException(errorMessage)))
                            }
                        }
                    }
                }
            })
        }
    }

    suspend fun getOfficeData(latitude: Double, longitude: Double): List<OfficeItem> {
        val url = link + "/get_office_location"

        val jsonBody = JSONObject().apply {
            put("latitude", latitude)
            put("longitude", longitude)
        }

        val requestBody =
            RequestBody.create(MediaType.parse("application/json"), jsonBody.toString())

        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()

        return suspendCoroutine { continuation ->
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    continuation.resumeWith(Result.failure(e))
                }

                override fun onResponse(call: Call, response: Response) {
                    response.use {
                        if (!response.isSuccessful) {
                            val errorMessage = "Response unsuccessful: ${response.code()}"
                            continuation.resumeWith(Result.failure(IOException(errorMessage)))
                        } else {
                            val jsonData = response.body()?.string()
                            if (jsonData != null) {
                                val officeItems = parseOfficeData(jsonData)
                                continuation.resumeWith(Result.success(officeItems))
                            } else {
                                val errorMessage = "Response body is empty"
                                continuation.resumeWith(Result.failure(IOException(errorMessage)))
                            }
                        }
                    }
                }
            })
        }
    }

    suspend fun getTime(
        latitudeUser: Double,
        longitudeUser: Double,
        latitudeVTB: Double,
        longitudeVTB: Double,
        type: Int
    ): String {
        val url = link + "/get_time"

        val jsonBody = JSONObject().apply {
            put("lat_p", latitudeUser)
            put("lon_p", longitudeUser)
            put("lat_vtb", latitudeVTB)
            put("lon_vtb", longitudeVTB)
            put("type_of_movement", type)

        }

        val requestBody =
            RequestBody.create(MediaType.parse("application/json"), jsonBody.toString())

        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()

        return suspendCoroutine { continuation ->
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    continuation.resumeWith(Result.failure(e))
                }

                override fun onResponse(call: Call, response: Response) {
                    response.use {
                        if (!response.isSuccessful) {
                            val errorMessage = "Response unsuccessful: ${response.code()}"
                            continuation.resumeWith(Result.failure(IOException(errorMessage)))
                        } else {
                            val jsonData = response.body()?.string()
                            if (jsonData != null) {
                                val officeItems = parseTime(jsonData)
                                continuation.resumeWith(Result.success(jsonData))
                            } else {
                                val errorMessage = "Response body is empty"
                                continuation.resumeWith(Result.failure(IOException(errorMessage)))
                            }
                        }
                    }
                }
            })
        }
    }

    private fun parseTime(jsonData: String): String {
        return jsonData
    }

    private fun parseAtmData(jsonData: String): List<AtmItem> {
        val atmItems = mutableListOf<AtmItem>()

        try {
            val jsonArray = JSONArray(jsonData)
            for (i in 0 until jsonArray.length()) {
                val jsonObject = jsonArray.getJSONObject(i)
                val address = jsonObject.getString("address")
                val latitude = jsonObject.getDouble("latitude")
                val longitude = jsonObject.getDouble("longitude")
                val allDay = jsonObject.getBoolean("allDay")

                atmItems.add(AtmItem(address, latitude, longitude, allDay))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        return atmItems
    }

    private fun parseOfficeData(jsonData: String): List<OfficeItem> {
        val officeItems = mutableListOf<OfficeItem>()

        try {
            val jsonArray = JSONArray(jsonData)
            for (i in 0 until jsonArray.length()) {
                val jsonObject = jsonArray.getJSONObject(i)
                val salePointName = jsonObject.getString("salePointName")
                val address = jsonObject.getString("address")
                val status = jsonObject.getString("status")
                val rko = jsonObject.getString("rko")
                val officeType = jsonObject.getString("officeType")
                val salePointFormat = jsonObject.getString("salePointFormat")
                val suoAvailability = jsonObject.getString("suoAvailability")
                val hasRamp = jsonObject.getString("hasRamp")
                val latitude = jsonObject.getDouble("latitude")
                val longitude = jsonObject.getDouble("longitude")
                val metroStation = jsonObject.getString("metroStation")
                val distance = jsonObject.getInt("distance")
                val kep = jsonObject.getBoolean("kep")
                val myBranch = jsonObject.getBoolean("myBranch")

                val openHoursArray = jsonObject.getJSONArray("openHours")
                val openHours = parseOpenHours(openHoursArray)

                val openHoursIndividualArray = jsonObject.getJSONArray("openHoursIndividual")
                val openHoursIndividual = parseOpenHours(openHoursIndividualArray)

                val officeItem = OfficeItem(
                    salePointName, address, status, openHours, rko, openHoursIndividual,
                    officeType, salePointFormat, suoAvailability, hasRamp, latitude, longitude,
                    metroStation, distance, kep, myBranch
                )

                officeItems.add(officeItem)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        return officeItems
    }

    private fun parseOpenHours(hoursArray: JSONArray): List<OpenHours> {
        val openHoursList = mutableListOf<OpenHours>()

        for (i in 0 until hoursArray.length()) {
            val hourObject = hoursArray.getJSONObject(i)
            val days = hourObject.getString("days")
            val hours = hourObject.getString("hours")
            val openHours = OpenHours(days, hours)
            openHoursList.add(openHours)
        }

        return openHoursList
    }
}
