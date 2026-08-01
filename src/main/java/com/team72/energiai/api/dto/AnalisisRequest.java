package com.team72.energiai.api.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class AnalisisRequest {

    @NotNull(message = "El consumo es obligatorio.")
    @Positive(message = "El consumo debe ser mayor que cero.")
    private Double consumoKwh;

    @NotNull(message = "Debe indicar si existe consumo en horario pico.")
    private Boolean usoHorarioPico;

    @NotNull(message = "La cantidad de equipos es obligatoria.")
    @Positive(message = "La cantidad de equipos debe ser mayor que cero.")
    private Integer cantidadEquipos;

    @NotBlank(message = "El tipo de inmueble es obligatorio.")
    private String tipoInmueble;

    @NotNull(message = "Las horas de alto consumo son obligatorias.")
    @PositiveOrZero(message = "Las horas de alto consumo no pueden ser negativas.")
    private Integer horasAltoConsumo;

    private Double superficieM2;
}