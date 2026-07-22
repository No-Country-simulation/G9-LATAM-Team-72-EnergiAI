package com.team72.energiai.api.dto;

import lombok.Data;

@Data
public class MLRequest {

    private Double consumoKwh;
    private Boolean usoHorarioPico;
    private Integer cantidadEquipos;
    private String tipoInmueble;
    private Integer horasAltoConsumo;
}
