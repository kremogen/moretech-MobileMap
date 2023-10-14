package com.example.moretechappmap

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import androidx.appcompat.app.AppCompatActivity

class SplashActivity : AppCompatActivity() {
    private val splashDelay = 2000

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)

        Handler().postDelayed({
            val mainIntent = Intent(this, MainActivity::class.java)
            startActivity(mainIntent)
            finish()
        }, splashDelay.toLong())
    }
}