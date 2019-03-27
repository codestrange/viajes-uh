<template>
    <div id="home">
        <div id="wrapper">
            <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">
                <router-link :to="{name: 'homePage'}" class="sidebar-brand d-flex align-items-center justify-content-center" href="">
                    <div class="sidebar-brand-icon rotate-n-15">
                        <i class="fas fa-calendar-alt"></i>
                    </div>
                </router-link>
                <hr class="sidebar-divider my-0">
                <li class="nav-item">
                    <router-link :to="{name: 'homePage'}" class="nav-link">
                        <i class="fas fa-fw fa-home"></i>
                        <span>Inicio</span></router-link>
                </li>
                <hr class="sidebar-divider">
            </ul>
            <div id="content-wrapper" class="d-flex flex-column">
                <div id="content">
                    <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
                        <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
                            <i class="fa fa-bars"></i>
                        </button>
                        <h1 class="h2 mb-0 text-dark">
                            UH Travels
                        </h1>
                        <ul class="navbar-nav ml-auto">
                            <li class="nav-item dropdown no-arrow mx-1">
                                <a class="nav-link dropdown-toggle" href="#" id="alertsDropdown" role="button"
                                   data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <i class="fas fa-bell fa-fw"></i>
                                    <!-- <span class="badge badge-danger badge-counter">2</span> -->
                                </a>
                                <div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in"
                                     aria-labelledby="alertsDropdown">
                                    <h6 class="dropdown-header text-center">
                                        Notificaciones
                                    </h6>
                                    <!-- <a class="dropdown-item d-flex align-items-center" href="#">
                                        <div class="mr-3">
                                            <div class="icon-circle bg-primary">
                                                <i class="fas fa-file-alt text-white"></i>
                                            </div>
                                        </div>
                                        <div>
                                            <div class="small text-gray-500">12 de diciembre del 2019</div>
                                            <span class="font-weight-bold">Un nuevo reporte esta listo para ser descargado</span>
                                        </div>
                                    </a>
                                    <a class="dropdown-item d-flex align-items-center" href="#">
                                        <div class="mr-3">
                                            <div class="icon-circle bg-success">
                                                <i class="fas fa-donate text-white"></i>
                                            </div>
                                        </div>
                                        <div>
                                            <div class="small text-gray-500">7 de diciembre del 2019</div>
                                            290.29 dolares han sido depositados en su cuenta.
                                        </div>
                                    </a> -->
                                    <span class="dropdown-item text-center text-dark">No hay notificaciones nuevas</span>
                                    <a class="dropdown-item text-center small text-gray-500" href="#">Ver todas las notificaciones</a>
                                </div>
                            </li>
                            <div class="topbar-divider d-none d-sm-block"></div>
                            <li class="nav-item dropdown no-arrow">
                                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button"
                                   data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <span class="mr-3 d-none d-lg-inline text-gray-600 small">{{ username }}</span>
                                    <img class="img-profile rounded-circle" :src="user_pic_location">
                                </a>
                                <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in"
                                     aria-labelledby="userDropdown">
                                    <router-link :to="{name: 'profilePage'}" class="dropdown-item">
                                        <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                                        Perfil
                                    </router-link>
                                    <!-- <a class="dropdown-item" href="#">
                                        <i class="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"></i>
                                        Configuración
                                    </a> -->
                                    <div class="dropdown-divider"></div>
                                    <a class="dropdown-item" href="#" data-toggle="modal" data-target="#logoutModal">
                                        <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                                        Cerrar Sesión
                                    </a>
                                </div>
                            </li>
                        </ul>
                    </nav>
                    <div class="container-fluid">
                        <router-view></router-view>
                    </div>
                </div>
                <hr>
                <footer class="sticky-footer bg-white">
                    <div class="container my-auto">
                        <div class="copyright text-center my-auto">
                            <strong>Facultad de Matemática y Computación de la Universidad de La Habana &copy; 2019</strong>
                        </div>
                    </div>
                </footer>
            </div>
        </div>
        <!-- <a class="scroll-to-top rounded" href="#page-top">
            <i class="fas fa-angle-up"></i>
        </a> -->
        <div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
             aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">¿Está seguro que desea cerrar sesión?</h5>
                        <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">x</span>
                        </button>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancelar</button>
                        <button class="btn btn-primary" data-dismiss="modal" @click="logoutUser">Cerrar Sesión</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Home",
        data() {
            return {
                loginOut: false,
                user_pic_location: './img/default_user_image.jpeg',
                username: ''
            };
        },
        methods: {
            logoutUser() {
                this.$store.state.profile.logOut();
                this.$router.push({ name: 'loginPage' });
            },
            openNewTab(url) {
                window.open(url, '_blank');
            }
        },
        created() {
            this.$store.state.profile.getData().then(() => {
                this.username = this.$store.state.profile.data.username;
            });
        }
    }
</script>
