
import customtkinter
import os
from PIL import Image

class ImageInst:
    def __init__(self) -> None:
        # load images with light and dark mode image
        image_path = os.path.join(os.getcwd(), "img")
        self.image_icon_app_design = customtkinter.CTkImage(Image.open(os.path.join(image_path, "app_design.png")), size=(20, 20))
        self.image_icon_color_wheel = customtkinter.CTkImage(Image.open(os.path.join(image_path, "color_wheel.png")), size=(20, 20))
        self.image_0 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_0_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_0_light.png")), size=(20, 20))
        self.image_1 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_1_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_1_light.png")), size=(20, 20))
        self.image_2 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_2_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_2_light.png")), size=(20, 20))
        self.image_3 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_3_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_3_light.png")), size=(20, 20))
        self.image_4 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_4_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_4_light.png")), size=(20, 20))
        self.image_5 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_5_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_5_light.png")), size=(20, 20))
        self.image_6 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_6_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_6_light.png")), size=(20, 20))
        self.image_7 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_7_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_7_light.png")), size=(20, 20))
        self.image_8 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_8_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_8_light.png")), size=(20, 20))
        self.image_9 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_9_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_9_light.png")), size=(20, 20))
        self.image_add = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_add_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_add_light.png")), size=(20, 20))
        self.image_add_dir = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_add_dir_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_add_dir_light.png")), size=(20, 20))
        self.image_add_file = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_add_file_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_add_file_light.png")), size=(20, 20))
        self.image_add_server = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_add_server_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_add_server_light.png")), size=(20, 20))
        self.image_add_user = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_add_user_light.png")), size=(20, 20))
        self.image_a = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_a_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_a_light.png")), size=(20, 20))
        self.image_b = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_b_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_b_light.png")), size=(20, 20))
        self.image_chat = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_chat_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_chat_light.png")), size=(20, 20))
        self.image_c = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_c_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_c_light.png")), size=(20, 20))
        self.image_delete = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_delete_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_delete_light.png")), size=(20, 20))
        self.image_detail = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_detail_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_detail_light.png")), size=(20, 20))
        self.image_directory = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_directory_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_directory_light.png")), size=(20, 20))
        self.image_doll = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_doll_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_doll_light.png")), size=(20, 20))
        self.image_d = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_d_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_d_light.png")), size=(20, 20))
        self.image_edit = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_edit_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_edit_light.png")), size=(20, 20))
        self.image_e = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_e_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_e_light.png")), size=(20, 20))
        self.image_file = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_file_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_file_light.png")), size=(20, 20))
        self.image_font = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_font_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_font_light.png")), size=(20, 20))
        self.image_f = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_f_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_f_light.png")), size=(20, 20))
        self.image_g = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_g_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_g_light.png")), size=(20, 20))
        self.image_height = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_height_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_height_light.png")), size=(20, 20))
        self.image_home = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_home_light.png")), size=(20, 20))
        self.image_h = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_h_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_h_light.png")), size=(20, 20))
        self.image_i = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_i_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_i_light.png")), size=(20, 20))
        self.image_j = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_j_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_j_light.png")), size=(20, 20))
        self.image_k = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_k_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_k_light.png")), size=(20, 20))
        self.image_lang = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_lang_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_lang_light.png")), size=(20, 20))
        self.image_l = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_l_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_l_light.png")), size=(20, 20))
        self.image_m = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_m_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_m_light.png")), size=(20, 20))
        self.image_n = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_n_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_n_light.png")), size=(20, 20))
        self.image_other = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_other_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_other_light.png")), size=(20, 20))
        self.image_o = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_o_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_o_light.png")), size=(20, 20))
        self.image_pen = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_pen_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_pen_light.png")), size=(20, 20))
        self.image_plus = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_plus_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_plus_light.png")), size=(20, 20))
        self.image_power = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_power_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_power_light.png")), size=(20, 20))
        self.image_p = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_p_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_p_light.png")), size=(20, 20))
        self.image_q = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_q_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_q_light.png")), size=(20, 20))
        self.image_r = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_r_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_r_light.png")), size=(20, 20))
        self.image_server = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_server_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_server_light.png")), size=(20, 20))
        self.image_setting = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_setting_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_setting_light.png")), size=(20, 20))
        self.image_s = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_s_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_s_light.png")), size=(20, 20))
        self.image_t = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_t_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_t_light.png")), size=(20, 20))
        self.image_u = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_u_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_u_light.png")), size=(20, 20))
        self.image_v = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_v_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_v_light.png")), size=(20, 20))
        self.image_width = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_width_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_width_light.png")), size=(20, 20))
        self.image_w = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_w_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_w_light.png")), size=(20, 20))
        self.image_x = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_x_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_x_light.png")), size=(20, 20))
        self.image_yen = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_yen_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_yen_light.png")), size=(20, 20))
        self.image_y = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_y_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_y_light.png")), size=(20, 20))
        self.image_z = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "image_z_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "image_z_light.png")), size=(20, 20))
        self.image_icon_logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(20, 20))
        self.image_icon_script = customtkinter.CTkImage(Image.open(os.path.join(image_path, "script.png")), size=(20, 20))
imginst = ImageInst()
