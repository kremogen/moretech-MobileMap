import com.yandex.mapkitdemo.placemark.AtmItem
import okhttp3.*
import org.json.JSONArray
import java.io.IOException
import kotlin.coroutines.suspendCoroutine

class MyApiService {
    private val client = OkHttpClient()

    suspend fun getAtmData(): List<AtmItem> {
        val url = "http://192.168.1.4:8000/get_atm" // Замените на ваш URL

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
}
