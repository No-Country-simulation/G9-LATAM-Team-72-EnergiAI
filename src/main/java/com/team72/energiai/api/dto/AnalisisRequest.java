package com.team72.energiai.api.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.Data;

@Data
@Schema(description = "Información enviada para realizar el análisis energético.")
public class AnalisisRequest {

    @Schema(
            description = "Consumo mensual de energía en kWh.",
            example = "350.5"
    )
    @NotNull(message = "El consumo es obligatorio.")
    @Positive(message = "El consumo debe ser mayor que cero.")
    private Double consumoKwh;

    @Schema(
            description = "Indica si existe consumo durante horario pico.",
            example = "true"
    )
    @NotNull(message = "Debe indicar si existe consumo en horario pico.")
    private Boolean usoHorarioPico;

    @Schema(
            description = "Cantidad total de equipos eléctricos.",
            example = "12"
    )
    @NotNull(message = "La cantidad de equipos es obligatoria.")
    @Positive(message = "La cantidad de equipos debe ser mayor que cero.")
    private Integer cantidadEquipos;

    @Schema(
            description = "Tipo de inmueble.",
            example = "Casa",
            allowableValues = {
                    "Casa",
                    "Comercio"
            }
    )
    @NotBlank(message = "El tipo de inmueble es obligatorio.")
    private String tipoInmueble;

    @Schema(
            description = "Horas promedio de alto consumo durante el día.",
            example = "6"
    )
    @NotNull(message = "Las horas de alto consumo son obligatorias.")
    @PositiveOrZero(message = "Las horas de alto consumo no pueden ser negativas.")
    private Integer horasAltoConsumo;

    @Schema(
            description = "Superficie del inmueble en metros cuadrados. Para viviendas puede omitirse.",
            example = "120"
    )
    private Double superficieM2;
}