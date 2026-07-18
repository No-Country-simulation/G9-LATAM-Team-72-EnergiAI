package com.team72.energiai.api.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public class AnalisisRequest {

    @NotNull
    @Min(1)
    private Double consumoMensual;

    @NotNull
    @Min(1)
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