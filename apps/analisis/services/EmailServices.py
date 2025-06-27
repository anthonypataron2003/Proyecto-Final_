import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Servicio para envío de análisis por email"""
    
    @staticmethod
    def enviar_analisis(analisis, destinatario, asunto=None, mensaje_personalizado=None, 
                       incluir_imagen=True, incluir_recomendaciones=True):
        """
        Envía un análisis nutricional por email
        
        Args:
            analisis: Instancia de AnalisisNutricional
            destinatario: Email del destinatario
            asunto: Asunto del email (opcional)
            mensaje_personalizado: Mensaje adicional (opcional)
            incluir_imagen: Si incluir la imagen analizada
            incluir_recomendaciones: Si incluir recomendaciones
            
        Returns:
            dict: {'exito': bool, 'mensaje': str}
        """
        try:
            if not asunto:
                estado = analisis.get_estado_nutricional_display()
                asunto = f'Análisis Nutricional - {analisis.nombre_paciente} ({estado})'
            
            context = {
                'analisis': analisis,
                'mensaje_personalizado': mensaje_personalizado,
                'incluir_recomendaciones': incluir_recomendaciones,
                'fecha_envio': analisis.fecha_analisis.strftime('%d/%m/%Y %H:%M'),
                'confianza_porcentaje': f"{analisis.confianza * 100:.1f}%" if analisis.confianza else "N/A"
            }
            
            html_content = render_to_string('email/analisis_email.html', context)
            text_content = strip_tags(html_content)
            
            email = EmailMessage(
                subject=asunto,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[destinatario],
            )
            email.content_subtype = "html"
            
            if incluir_imagen and analisis.imagen:
                try:
                    if os.path.exists(analisis.imagen.path):
                        email.attach_file(analisis.imagen.path)
                    else:
                        logger.warning(f'Imagen no encontrada: {analisis.imagen.path}')
                except Exception as e:
                    logger.error(f'Error adjuntando imagen: {e}')
            
            email.send()
            
            logger.info(f'Análisis {analisis.id} enviado por email a {destinatario}')
            
            return {
                'exito': True,
                'mensaje': f'Análisis enviado exitosamente a {destinatario}'
            }
            
        except Exception as e:
            error_msg = f'Error enviando email: {str(e)}'
            logger.error(error_msg)
            return {
                'exito': False,
                'mensaje': error_msg
            }