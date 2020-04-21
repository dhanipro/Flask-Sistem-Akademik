
          $('.button-hapus').on('click', function(){
            $('.modal').addClass('is-active');
            console.log($(this).data('id'));
            var id = $(this).data('id');
            var title = $('.title#'+id).text();
            console.log(title);
            $('.modal-card-body').text(title)
          })
          $(".delete").click(function() {
            $(".modal").removeClass("is-active");
          });


            //modal delete siswa
            $('.modal-delete-siswa').on('click', function() {
              $('.modal-hapus-siswa').addClass('is-active');
              var id = $(this).data('siswa');
              var namaSiswa = $('.nama-siswa'+id).text();
              $('.id-siswa').text(namaSiswa)
              $('#hapus-siswa').attr('action', '/siswa/delete/'+id);

              $(".cancel-button-hapus-siswa").click(function() {
                $(".modal-hapus-siswa").removeClass("is-active");
              });
            })

            //modal detail siswa
            $('.detail-siswa').on('click', function() {
                $('.modal-detail-siswa').addClass('is-active');
                var id = $(this).data('siswa');
                $.ajax({
                    url: '/siswa/detail/'+id,
                    success: data => {
                        const modalSiswa = `<div class="columns">
                                                <div class="column">
                                                    <img src="${data.image}">
                                                </div>
                                                <div class="column is-8">
                                                    <table class="table is-narrow">
                                                        <tr>
                                                            <td>Kelas</td>
                                                            <td>:</td>
                                                            <td>${data.kelas}</td>
                                                        </tr>
                                                        <tr>
                                                            <td>Lahir</td>
                                                            <td>:</td>
                                                            <td>${data.lahir}</td>
                                                        </tr>
                                                        <tr>
                                                            <td>Jenis Kelamin</td>
                                                            <td>:</td>
                                                            <td>${data.kelamin}</td>
                                                        </tr>
                                                        <tr>
                                                            <td>Agama</td>
                                                            <td>:</td>
                                                            <td>${data.agama}</td>
                                                        </tr>
                                                        <tr>
                                                            <td>Alamat</td>
                                                            <td>:</td>
                                                            <td><span class="is-size-7">${data.alamat}</span></td>
                                                        </tr>
                                                    </table>
                                                    <a href="/siswa/data-absen/${data.id}" class="button is-info is-small">Lihat Absensi</a>
                                                </div>
                                            </div>`;
                        $('.modal-detail-siswa .modal-card-body').html(modalSiswa);
                    }
                })
                // $.getJSON('/siswa/detail/'+id, function(data) {
                //     console.log(data.agama)
                // });

                var namaSiswa = $('.nama-siswa'+id).text();
                $('.modal-card-title').text(namaSiswa)
  
                $(".cancel-button-detail-siswa").click(function() {
                  $(".modal-detail-siswa").removeClass("is-active");
                });
              })

              //modal update spp
                $('.modal-update').on('click', function() {
                    $('.modal-update-spp').addClass('is-active');
                    var id = $(this).data('siswa');
                    $('#update-siswa-spp').attr('action', '/update-spp/'+id);

                    $(".cancel-button-update-spp").click(function() {
                        $(".modal-update-spp").removeClass("is-active");
                      });
                });