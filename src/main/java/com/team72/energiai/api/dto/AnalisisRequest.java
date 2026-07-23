package com.team72.energiai.api.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public class AnalisisRequest {

    @NotNull(message = "El consumo mensual es obligatorio.")
    @Min(value = 1, message = "El consumo mensual debe ser mayor que cero.")
    private Double consumoMensual;

    @NotNull(message = "La cantidad de equipos es obligatoria.")
    @Min(value = 1, message = "La cantidad de equipos debe ser mayor que cero.")
    private Integer cantidadEquipos;

    public Double getConsumoMensual() {
        return consumoMensual;
    }

    public void setConsumoMensual(Double consumoMensual) {
        this.consumoMensual = consumoMensual;
    }

    public Integer getCantidadEquipos() {
        return cantidadEquipos;
    }

    public void setCantidadEquipos(Integer cantidadEquipos) {
        this.cantidadEquipos = cantidadEquipos;
    }
}