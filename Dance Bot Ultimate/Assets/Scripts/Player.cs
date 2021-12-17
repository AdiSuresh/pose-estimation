using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{

    public float speed = 5;
    public float turnSpeed = 2.5f;

    public Animator anim;

    // Update is called once per frame
    void Update()
    {
        float strafe = Input.GetAxis("Horizontal");
        float forward = Input.GetAxis("Vertical");
        float turn = Input.GetAxis("Mouse X");

        // To move the robot in all directions
        transform.Translate(new Vector3(strafe, 0, forward) * speed * Time.deltaTime);
        // To rotate the robot in all directions
        transform.rotation *= Quaternion.Slerp(Quaternion.identity, Quaternion.LookRotation(turn < 0? Vector3.left : Vector3.right), Mathf.Abs(turn) * turnSpeed * Time.deltaTime);

        anim.SetFloat("Forward", forward);
        anim.SetFloat("Right", strafe);
    }
}
