import { useState } from "react";
import { LocateFixed, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { trackJctEvent } from "@/lib/analytics";

type Props = {
  onLocation: (value: { lat: number; lng: number; accuracy: number }) => void;
};

export function GetMyLocationButton({ onLocation }: Props) {
  const [state, setState] = useState<"idle" | "loading" | "denied" | "error" | "done">("idle");

  function requestLocation() {
    trackJctEvent("get_location_click");
    if (!navigator.geolocation) {
      setState("error");
      return;
    }
    setState("loading");
    navigator.geolocation.getCurrentPosition(
      (p) => {
        onLocation({ lat: p.coords.latitude, lng: p.coords.longitude, accuracy: p.coords.accuracy });
        setState("done");
        trackJctEvent("geolocation_granted", { accuracy_m: Math.round(p.coords.accuracy) });
      },
      (e) => {
        setState(e.code === e.PERMISSION_DENIED ? "denied" : "error");
        trackJctEvent("geolocation_denied", { code: e.code });
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 },
    );
  }

  return (
    <div>
      <Button type="button" variant="inverse" onClick={requestLocation} disabled={state === "loading"}>
        {state === "loading" ? <Loader2 className="animate-spin" /> : <LocateFixed />}
        {state === "done" ? "Location added" : "Use my current location"}
      </Button>
      {state === "denied" && <p className="mt-2 text-sm text-muted-foreground">Location access was not allowed. Enter an address, intersection, or landmark instead.</p>}
      {state === "error" && <p className="mt-2 text-sm text-muted-foreground">We could not get your location. Enter it manually instead.</p>}
    </div>
  );
}
