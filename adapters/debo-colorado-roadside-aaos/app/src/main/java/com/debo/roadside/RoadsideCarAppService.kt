package com.debo.roadside

import android.content.Intent
import android.content.pm.ApplicationInfo
import android.net.Uri
import androidx.car.app.CarAppService
import androidx.car.app.CarContext
import androidx.car.app.CarToast
import androidx.car.app.Screen
import androidx.car.app.Session
import androidx.car.app.model.Action
import androidx.car.app.model.ItemList
import androidx.car.app.model.ListTemplate
import androidx.car.app.model.Row
import androidx.car.app.model.Template
import androidx.car.app.validation.HostValidator

/** Driver-optimized roadside points of interest. Does not read or store vehicle telemetry. */
class RoadsideCarAppService : CarAppService() {
    override fun createHostValidator(): HostValidator {
        val debug = (applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) != 0
        return if (debug) {
            HostValidator.ALLOW_ALL_HOSTS_VALIDATOR
        } else {
            HostValidator.Builder(this)
                .addAllowedHosts(androidx.car.app.R.array.hosts_allowlist_sample)
                .build()
        }
    }

    override fun onCreateSession(): Session = object : Session() {
        override fun onCreateScreen(intent: Intent): Screen = RoadsidePlacesScreen(carContext)
    }
}

internal data class PlaceCategory(val title: String, val description: String, val mapQuery: String)

internal class RoadsidePlacesScreen(context: CarContext) : Screen(context) {
    private val categories = listOf(
        PlaceCategory("Fuel stations", "Find nearby gasoline stations", "gas station near me"),
        PlaceCategory("Tire service", "Find nearby tire repair and shops", "tire repair near me"),
        PlaceCategory("Auto repair", "Find nearby vehicle service shops", "auto repair near me"),
        PlaceCategory("Auto parts", "Find nearby parts suppliers", "auto parts store near me")
    )

    override fun onGetTemplate(): Template {
        val list = ItemList.Builder()
        for (place in categories) {
            list.addItem(Row.Builder()
                .setTitle(place.title)
                .addText(place.description)
                .setOnClickListener { findWithMaps(place.mapQuery) }
                .build())
        }
        return ListTemplate.Builder()
            .setTitle("DEBO Roadside")
            .setHeaderAction(Action.APP_ICON)
            .setSingleList(list.build())
            .build()
    }

    private fun findWithMaps(query: String) {
        val uri = Uri.parse("geo:0,0?q=" + Uri.encode(query))
        val intent = Intent(CarContext.ACTION_NAVIGATE, uri)
        try {
            carContext.startCarApp(intent)
        } catch (_: Exception) {
            CarToast.makeText(carContext, "Navigation app unavailable", CarToast.LENGTH_SHORT).show()
        }
    }
}
